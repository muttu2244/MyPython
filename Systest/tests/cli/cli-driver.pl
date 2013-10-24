#!/usr/bin/perl -w

use strict;
use warnings;
use warnings FATAL => qw(all); # we don't want any warnings to go unnoticed
use Getopt::Std;

use Expect;
use Math::BigInt lib => 'GMP';
use IO::File;

use vars qw ($System $Command $Timeout $Exp %Default %Custom %Ignore);
use vars qw ($InitMode $CmdLog);
use vars qw ($DecIntMin $DecIntMax $DecUintMax $HexUintMax $CommMax);
use vars qw ($StrLenMax);
use vars qw ($opt_h $opt_c $opt_f $opt_l $opt_C $opt_t $opt_s $opt_i);
use vars qw ($opt_n $opt_N $opt_a $opt_2 $opt_L $opt_r $opt_S $opt_u);
use vars qw ($opt_p $opt_V $opt_z);

getopts('hcf:l:C:t:si:nNa2L:rS:u:p:Vz');

# function prototypes (allows perl to check each function call)
sub usage();
sub doit();
sub proc_cmd_opts($$$);
sub log_cmd($);
sub exec_cmd($$$);
sub my_exp($$);
sub get_cus_vals($);
sub get_def_vals($$$$$;$$);
sub get_opt_vals($$$$$$;$$);
sub get_opt_vals_dec_uint($$$);
sub get_val_dec_uint($$$);
sub get_opt_vals_dec_int($$$);
sub get_val_dec_int($$$);
sub get_opt_vals_hex_uint($$$);
sub get_val_hex_uint($$$);
sub get_opt_vals_ipv4_addr($);
sub ipv4_addr_txt2bin($);
sub ipv4_addr_bin2txt($);
sub get_opt_vals_ipv4_mask($);
sub get_opt_vals_ipv4_addr_mask($);
sub get_opt_vals_ipv6_addr($);
sub get_opt_vals_ipv6_mask($);
sub get_opt_vals_ipv6_addr_mask($);
sub get_opt_vals_ether($);
sub get_opt_vals_string($$);
sub get_opt_vals_slot($$$);
sub get_opt_vals_slot_port($$$$$);
sub get_opt_vals_slot_port_chan($$$$$$$);
sub get_opt_vals_comm($$$$$);
sub get_val_comm_low_high($$$);
sub get_val_comm($$$);
sub get_show_config();

# option checking
if ($opt_h) {
    usage();
}
if ($opt_N && ($opt_n || $opt_a || $opt_2)) {
    print "Option -N can not be specified with -n, -a or -2.\n";
    exit(0);
}
if (!$opt_c && !$opt_C) {
    print "Option -c or -C must be specified.\n";
    exit(0);
}
if ($opt_s && !$opt_l) {
    print "When suppressing output (-s), logging must be enabled (-l).\n";
    exit(0);
}
if ($opt_r && !$opt_c) {
    print "Option -r must be used with -c.\n";
    exit(0);
}
if ($opt_S) {
    unless ($opt_S =~ /^\d+$/) {
        print "Option -S must contain only digits\n";
        exit(0);
    }
    if ($opt_S < 1 || $opt_S > 7) {
        print "Bad option -S value\n";
        exit(0);
    }
}
if ($opt_u && !$opt_p) {
    print "Option -u also requires -p to be specified\n";
    exit(0);
}
if ($opt_p && !$opt_u) {
    print "Option -p can not be specified without $opt_u\n";
    exit(0);
}
if (scalar(@ARGV) != 1) {
    print "No system specified.\n";
    exit(0);
}

if ($opt_V) {
    if (!$opt_c || !$opt_n) {
        print "-V is only allowed with -c and -n\n";
        exit(0);
    }
    if ($opt_r || $opt_2) {
        print "-V not allowed with -r, -2\n";
        exit(0);
    }
}

# global variable initialisation
$System     = shift(@ARGV);
$Timeout    = $opt_t ? $opt_t : 60; # default to 10 seconds
$InitMode   = 2;                    # configuration starts at mode index 2

$DecIntMin  = -2147483648;
$DecIntMax  = 2147483647;
$DecUintMax = '4294967295';
$HexUintMax = 'ffffffff';
$CommMax    = 65535;
$StrLenMax  = 132;

# the main function
doit();

sub usage()
{
    print "Usage:\n";
    print " cli-driver.pl [...options...] <system>\n";
    print "  system       target system to use\n";
    print "  -c           configuration mode (default is exe mode)\n";
    print "  -C command   CLI command at which to start testing\n";
    print "  -i commands  initial commands to execute (separated by '::')\n";
    print "  -n           always remove configuration before adding\n";
    print "  -a           remove configuration after adding\n";
    print "  -2           remove configuration twice\n";
    print "  -N           never remove configuration\n";
    print "  -r           repeat each config command; and check for no error\n";
    print "  -V           verify each config command exists in show config\n";
    print "  -S level     show hidden commands for the specified level\n";
    print "  -f file      driver data file\n";
    print "  -l file      log file\n";
    print "  -L file      command log file\n";
    print "  -t secs      command response timeout (default is 10)\n";
    print "  -s           suppress output to stdout\n";
    print "  -u username  username for Stoke stack login\n";
    print "  -p password  password for Stoke stack login\n";
    print "  -z           assume <system> is console with no authentication\n";

    exit(0);
}

sub doit()
{
    init();

    $Exp = Expect->spawn('telnet', $System);

    if ($opt_s) {
        $Exp->log_stdout(0);
    }

    if ($opt_u) {
        my_exp('', 'Username:');
        my_exp("$opt_u\n", 'assword:');
        my_exp("$opt_p\n", '#');
    } elsif ($opt_z) {
        my_exp(undef, "Escape character");
        $Exp->send("\n");
        my @res = $Exp->expect($Timeout, '#', 'option');
        if (defined($res[1])) {
            if ($res[1] eq '1:TIMEOUT') {
                die "\nTimeout awaiting: '#' or 'option'\n";
            } else {
                die "\nUnexpected expect error: $res[1]\n";
            }
        }
        if ($res[0] == 2) {
            my_exp("1\n", '#');
        }
        @res = my_exp("\n", '#');
        if ($res[3] =~ /\(cfg/) {
            my_exp("end\n", '#');
        }
    } else {
        my_exp('', 'login:');
        my_exp("root\n", '#');
        my_exp("cli -I; echo ===CLI Terminated===\n", '#');
    }
    my_exp("terminal length infinite\n", '#');
    my_exp("terminal width infinite\n", '#');
    my_exp("terminal driver-test <<<<help_begin >>>>help_end\n", '#');

    if ($opt_S) {
        my $time = time;
        if (&try_pwd($time)) {
            my $sec_per_day = 60 * 60 * 24;
            $time -= $sec_per_day;
            if (&try_pwd($time)) {
                $time += ($sec_per_day * 2);
                if (&try_pwd($time)) {
                    die "\Unable to enter hidden show password\n";
                }
            }
        }
    }

    my @res;

    if ($opt_V) {
        my_exp("clear config\n", '?');
        my_exp("yes\n", '#');
        @res = my_exp("show config | count\n", '#');
        unless ($res[3] =~ /Count: (\d+)/ && $1 == 2) {
            die "\nUnable to clear configuration\n";
        }
    }

    if ($opt_c) {
        my_exp("configuration\n", '#');
    }

    my (%hist);
    if ($opt_i) {
        my @cmds = split(/::/, $opt_i);
        my $cmd;
        foreach $cmd (@cmds) {
            $cmd =~ s/_/ /g;
            @res = my_exp("$cmd\n", '#');
            if ($opt_c) {
                $res[3] =~ /\(cfg\-(\d+)\)/;
                my $mode = $1;
                if ($mode != $InitMode) {
                    $InitMode = $mode;
                    if (defined($hist{"mode_cmds"})) {
                        $hist{"mode_cmds"} .= "__$cmd";
                    } else {
                        $hist{"mode_cmds"} = $cmd;
                    }
                }
            }
        }
    }

    if ($opt_l) {
        $Exp->log_file($opt_l, "w");
    }

    if ($opt_L) {
        $CmdLog = IO::File->new("> $opt_L") or
            die "Unable to open $opt_L: $!\n";
    }

    proc_cmd_opts($Command, $InitMode, \%hist);

    $Exp->hard_close();

    print "\n\nCLI driver script completed.\n";
}

sub try_pwd()
{
    my ($time_arg) = @_;

    my @time = gmtime($time_arg);
    my $yyyy = $time[5] + 1900;
    my $mm   = $time[4] + 1;
    my $dd   = $time[3];
    my $pwd  = $yyyy + $mm + ($dd * $opt_S);
    my_exp("hidden show $opt_S\n", 'Password: ');
    my @res = my_exp("$pwd\n", '#');
    if ($res[3] =~ /Invalid/) {
        return (-1);
    } else {
        return (undef);
    }
}

sub init()
{
    if ($opt_C) {
        $Command = $opt_C;
        $Command =~ s/^\"//;
        $Command =~ s/\"$//;
        $Command =~ s/_/ /g;
    } else {
        $Command = '';
    }

    return unless defined $opt_f;

    my (@opts) = ('decimal-uint', 'decimal-int', 'hex-uint',
                  'ipv4-address', 'ipv4-mask',
                  'ipv6-address', 'ipv6-mask',
                  'string', 'slot', 'port', 'slot-port',
                  'slot-port-chan', 'community');

    open(FILE, $opt_f) or die "unable to open $opt_f: $!\n";
    my ($state_init, $state_default, $state_custom, $state_ignore) =
        (1, 2, 3, 4);
    my $state = $state_init;
    my $line  = 0;
    my $custom_cmd;
    while (<FILE>) {
        $line++;
        chomp;
        next if /^\s*$/;
        next if /^\#/;
        s/\s*$//; # remove trailing spaces
        if (/^default:$/) {
            $state = $state_default;
            next;
        } elsif (/^custom:$/) {
            $state = $state_custom;
            next;
        } elsif (/^ignore:$/) {
            $state = $state_ignore;
            next;
        } elsif (/^[^ ]/) {
            die "\nLine $line; unexpected 1st column directive: $_\n";
        }
        if ($state == $state_init) {
            die "\nLine $line; option without a directive: $_\n";
        } elsif ($state == $state_default) {
            s/^\s+//;
            my ($opt, $args) = split(/\s+/, $_, 2);
            unless (grep(/^$opt$/, @opts)) {
                die "\nLine $line; unsupported option: $opt\n";
            }
            $Default{$opt} = $args;
        } elsif ($state == $state_custom) {
            s/^\s*//g;
            if (/^:?[\w\-\.]+:$/) {
                # custom command
                s/:$//;
                s/_/ /g;
                $custom_cmd = $_;
                if (/^:/) {
                    s/^://;
                    if (defined($Custom{':mode_cmds:'})) {
                        $Custom{':mode_cmds:'} .= "__${_}";
                    } else {
                        $Custom{':mode_cmds:'} = $_;
                    }
                }
                next;
            }
            # custom command options
            die "\nLine $line; options must follow a custom command\n"
                unless defined($custom_cmd);
            my $cmd = $custom_cmd;
            s/^\s+//;
            my ($opt, $args) = split(/\s+/, $_, 2);
            if ($opt =~ /^_/) {
                if ($opt eq '_line_') {
                    if (defined($Custom{$cmd})) {
                        $Custom{$cmd} .= "__$args";
                    } else {
                        $Custom{$cmd} = "_line__$args";
                    }
                } else {
                    die "\n Line $line; bad option: $opt\n";
                }
            } else {
                if (defined($Custom{$cmd})) {
                    $Custom{$cmd} .= "::::${opt}:::$args";
                } else {
                    $Custom{$cmd} = "_args__${opt}:::$args";
                }
            }
        } elsif ($state == $state_ignore) {
            s/^\s*//g;
            s/_/ /g;
            if (defined($Ignore{$_})) {
                die "\n Line $line; duplicate command: $_\n";
            } else {
                $Ignore{$_} = 1;
            }
        } else {
            die "\nLine $line; bad state: $state\n";
        }
    }
    close(FILE);
}

sub proc_cmd_opts($$$)
{
    my ($cmd, $mode, $hist) = @_;

    $cmd =~ s/^\s*//;

    my @vals;
    my $val;
    my $exit_needed = 0;
    if ($cmd eq '') {
        if ($opt_c) {
            my $cmc = $Custom{':mode_cmds:'};
            my $hmc = $$hist{'mode_cmds'};
            if (defined($cmc) && defined($hmc)) {
                my @hmcs = split(/__/, $hmc);
                my $last_mc = pop(@hmcs);
                my @cmcs = split(/__/, $cmc);
                foreach $cmc (@cmcs) {
                    if ($last_mc =~ /^${cmc}/) {
                        @vals = get_cus_vals(":$cmc");
                        $exit_needed = 1;
                    }
                }
            }
        }
    } else {
        if (defined($Ignore{$cmd})) {
            # ignore this command
            return;
        }
        if (defined($Custom{$cmd})) {
            # no need to check the available options - we've been given
            # explicit options to use
            @vals = get_cus_vals($cmd);
        }
    }
    if (scalar(@vals) > 0) {
        foreach $val (@vals) {
            if ($val =~ /\$$/) {
                $val =~ s/\$$//;
                exec_cmd("$cmd $val", $mode, $hist);
            } else {
                proc_cmd_opts("$cmd $val", $mode, $hist);
            }
        }
        if ($exit_needed) {
            log_cmd("exit\n");
            my_exp("\cuexit\n\cu<!>", "<!>");
            if ($$hist{'mode_cmds'} =~ /__/) {
                $$hist{'mode_cmds'} =~ s/__[a-z0-9 \-]+$//;
            } else {
                $$hist{'mode_cmds'} = undef;
            }
        }
        return;
    }

    # get help output for the current command
    my @res = my_exp("\cu$cmd ?\cu<!>", '<!>');
    if ($res[0] != 1) {
        return;
    }
    my $output = $res[3];
    $output =~ s/\r/\n/g;
    $output =~ s/\n\n/\n/g;
    $output =~ s/^\n*//;
    $output =~ s/\n*$//;
    my @opts = split(/\n/, $output);
    my $banner_start = 0;
    my $exit_found   = 0;
    foreach (@opts) {
        if (!$banner_start) {
            if (/^<<<<help_begin/) {
                $banner_start = 1;
            }
            next;
        }
        if (/^>>>>help_end/) {
            if ($opt_c) {
                if ($exit_found) {
                    log_cmd("exit\n");
                    my_exp("\cuexit\n\cu<!>", "<!>");
                    if (defined($$hist{'mode_cmds'})) {
                        if ($$hist{'mode_cmds'} =~ /__/) {
                            $$hist{'mode_cmds'} =~ s/__[a-z0-9 \-]+$//;
                        } else {
                            $$hist{'mode_cmds'} = undef;
                        }
                    }
                }
            }
            return;
        }
        if ($opt_c) {
            if (/^exit /) {
                $exit_found = 1;
                next;
            }
            if (/^(end|debug|show|no) /) {
                next;
            }
        }
        s/[\n\r]*//g;
        next if /^\s*$/;
        next if /^ /;
        next if /^\|/;
        next if /^[[:cntrl:]]/;
        next if /\w+\[\w+\]#/;

        my ($opt, $help) = split(/ \s+/, $_, 2);
        if ($opt =~ /^\<cr\>/) {
            # execute a command command
            exec_cmd($cmd, $mode, $hist);
        } elsif ($opt =~ /\.\./) {
            # value range
            if ($opt =~ /^SLOT\(/) {
                $opt =~ s/^SLOT\(//;
                $opt =~ s/\)$//;
                $opt =~ s/\.\./:/;
                my ($min, $max) = split(/:/, $opt);
                @vals = get_def_vals('slot', $min, $max, undef, undef);
                if (scalar(@vals) > 0) {
                    foreach (@vals) {
                        proc_cmd_opts("$cmd $_", $mode, $hist);
                    }
                } else {
                    proc_cmd_opts("$cmd 0", $mode, $hist);
                }
            } elsif ($opt =~ /^SLOTPORT\(/) {
                $opt =~ s/^SLOTPORT\(//;
                $opt =~ s/\)$//;
                $opt =~ s/\.\./:/g;
                $opt =~ s/\//:/;
                my ($min1, $max1, $min2, $max2) = split(/:/, $opt);
                @vals = get_def_vals('slot-port', $min1, $max1, $min2, $max2);
                if (scalar(@vals) > 0) {
                    foreach (@vals) {
                        proc_cmd_opts("$cmd $_", $mode, $hist);
                    }
                } else {
                    proc_cmd_opts("$cmd 0/0", $mode, $hist);
                }
            } elsif ($opt =~ /^SLOTPORTCHAN\(/) {
                $opt =~ s/^SLOTPORTCHAN\(//;
                $opt =~ s/\)$//;
                $opt =~ s/\.\./:/g;
                $opt =~ s/\//:/g;
                my ($min1, $max1, $min2, $max2, $min3, $max3) =
                    split(/:/, $opt);
                @vals = get_def_vals('slot-port-chan',
                                     $min1, $max1, $min2, $max2, $min3, $max3);
                if (scalar(@vals) > 0) {
                    foreach (@vals) {
                        proc_cmd_opts("$cmd $_", $mode, $hist);
                    }
                } else {
                    proc_cmd_opts("$cmd 0/0", $mode, $hist);
                }
            } elsif ($opt =~ /^(\d+)\.\.(\d+):(\d+)\.\.(\d+)$/) {
                # community number range
                my ($min1, $max1, $min2, $max2) = ($1, $2, $3, $4);
                @vals = get_def_vals('community', $min1, $max1, $min2, $max2);
                if (scalar(@vals) > 0) {
                    foreach $val (@vals) {
                        proc_cmd_opts("$cmd $val", $mode, $hist);
                    }
                } else {
                    my $val2;
                    if ($min1 > 1) {
                        $val = $min1;
                    } else {
                        $val = 1;
                    }
                    if ($min2 > 1) {
                        $val2 = $min2;
                    } else {
                        $val2 = 1;
                    }
                    proc_cmd_opts("$cmd ${val}:$val2", $mode, $hist);
                }
            } elsif ($opt =~ /^(\d+)\.\.(\d+)$/) {
                # unsigned decimal value range
                my ($min, $max) = ($1, $2);
                @vals = get_def_vals('decimal-uint', $min, $max, undef, undef);
                if (scalar(@vals) > 0) {
                    foreach $val (@vals) {
                        proc_cmd_opts("$cmd $val", $mode, $hist);
                    }
                } else {
                    $min = Math::BigInt->new($min);
                    if ($min > 1) {
                        $val = $min->bstr();
                    } else {
                        $val = 1;
                    }
                    proc_cmd_opts("$cmd $val", $mode, $hist);
                }
            } elsif ($opt =~ /^([\-]?\d+)\.\.([\-]?\d+)$/) {
                # signed decimal value range
                my ($min, $max) = ($1, $2);
                @vals = get_def_vals('decimal-int', $min, $max, undef, undef);
                if (scalar(@vals) > 0) {
                    foreach $val (@vals) {
                        proc_cmd_opts("$cmd $val", $mode, $hist);
                    }
                } else {
                    if ($min > 1) {
                        $val = $min;
                    } else {
                        $val = 1;
                    }
                    proc_cmd_opts("$cmd $val", $mode, $hist);
                }
            } elsif ($opt =~ /([[:xdigit:]]+)\.\.([[:xdigit:]]+)$/) {
                # unsigned hex value range
                my ($min, $max) = ($1, $2);
                @vals = get_def_vals('hex-uint', $min, $max, undef, undef);
                if (scalar(@vals) > 0) {
                    foreach $val (@vals) {
                        proc_cmd_opts("$cmd $val", $mode, $hist);
                    }
                } else {
                    $min = Math::BigInt->new("0x$min");
                    if ($min > 1) {
                        $val = $min->as_hex();
                        $val =~ s/^0x//;
                    } else {
                        $val = 1;
                    }
                    proc_cmd_opts("$cmd $val", $mode, $hist);
                }
            } elsif ($opt =~ /^(\d+)\.\.(\d+) or \d+\.\.\d+\-\d+\.\.\d+$/) {
                # number set
                my ($min, $max) = ($1, $2);
                proc_cmd_opts("$cmd $min", $mode, $hist);
            } else {
                die "\nUnable to handle range: '$opt'\n";
            }
        } elsif ($opt =~ /^n\.n\.n\.n$/) {
            # ipv4 address
            @vals = get_def_vals('ipv4-address', undef, undef, undef, undef);
            if (scalar(@vals) > 0) {
                foreach (@vals) {
                    proc_cmd_opts("$cmd $_", $mode, $hist);
                }
            } else {
                proc_cmd_opts("$cmd 1.1.1.1", $mode, $hist);
            }
        } elsif ($opt =~ /^n\.n\.n\.n or \/n$/) {
            # ipv4 mask
            @vals = get_def_vals('ipv4-mask', undef, undef, undef, undef);
            if (scalar(@vals) > 0) {
                foreach (@vals) {
                    proc_cmd_opts("$cmd $_", $mode, $hist);
                }
            } else {
                proc_cmd_opts("$cmd /24", $mode, $hist);
            }
        } elsif ($opt =~ /^n\.n\.n\.n\/n$/) {
            # ipv4 address and mask
            @vals = get_def_vals('ipv4-addr-mask', undef, undef, undef, undef);
            if (scalar(@vals) > 0) {
                foreach (@vals) {
                    proc_cmd_opts("$cmd $_", $mode, $hist);
                }
            } else {
                proc_cmd_opts("$cmd 1.1.1.1/24", $mode, $hist);
            }
        } elsif ($opt =~ /^x:x:x:x:x:x:x:x$/) {
            # ipv6 address
            @vals = get_def_vals('ipv6-address', undef, undef, undef, undef);
            if (scalar(@vals) > 0) {
                foreach (@vals) {
                    proc_cmd_opts("$cmd $_", $mode, $hist);
                }
            } else {
                proc_cmd_opts("$cmd 1::1", $mode, $hist);
            }
        } elsif ($opt =~ /^\/n$/) {
            # ipv6 mask
            @vals = get_def_vals('ipv6-mask', undef, undef, undef, undef);
            if (scalar(@vals) > 0) {
                foreach (@vals) {
                    proc_cmd_opts("$cmd $_", $mode, $hist);
                }
            } else {
                proc_cmd_opts("$cmd /64", $mode, $hist);
            }
        } elsif ($opt =~ /^x:x:x:x:x:x:x:x\/n$/) {
            # ipv6 address and mask
            @vals = get_def_vals('ipv6-addr-mask', undef, undef, undef, undef);
            if (scalar(@vals) > 0) {
                foreach (@vals) {
                    proc_cmd_opts("$cmd $_", $mode, $hist);
                }
            } else {
                proc_cmd_opts("$cmd 1::1/64", $mode, $hist);
            }
        } elsif ($opt =~ /^xx:xx:xx:xx:xx:xx$/) {
            # ethernet address
            @vals = get_def_vals('ethernet', undef, undef, undef, undef);
            if (scalar(@vals) > 0) {
                foreach (@vals) {
                    proc_cmd_opts("$cmd $_", $mode, $hist);
                }
            } else {
                proc_cmd_opts("$cmd 00:00:11:11:11:11", $mode, $hist);
            }
        } elsif ($opt =~ /^STRING/) {
            # string
            my $max;
            if ($opt ne 'STRING') {
                unless ($opt =~ /^STRING\((\d+)\)$/) {
                    die "\nUnable to handle CLI help output: $opt\n";
                }
                $max = $1;
            }
            @vals = get_def_vals('string', undef, $max, undef, undef);
            if (scalar(@vals) > 0) {
                foreach (@vals) {
                    proc_cmd_opts("$cmd $_", $mode, $hist);
                }
            } else {
                # choose 'local' to pick up the only string that
                # is always defined: context local
                proc_cmd_opts("$cmd local", $mode, $hist);
            }
        } elsif ($opt =~ /^[\w\-]+$/ || $opt =~ /^\*$/) {
            # regular keyword
            proc_cmd_opts("$cmd $opt", $mode, $hist);
        } else {
            die "\nUnable to handle command ($cmd) option '$opt'\n";
        }
    }
}

sub get_show_config()
{
    my @res = my_exp("\cushow config\n\cu<!>", '<!>');
    if ($res[0] != 1) {
        # command was not accepted
        die "\ncommand not accept: show config\n";
    }
    my $sc_line = $res[3];
    $sc_line =~ s/\r\n/\n/g;
    $sc_line =~ s/\n\r/\n/g;
    $sc_line =~ s/ *\n/\n/g;
    my @sc = split(/[\n]/, $sc_line);
    pop(@sc);
    shift(@sc);
    return (@sc);
}

sub exec_cmd($$$)
{
    my ($cmd, $mode, $hist) = @_;

    my (@res, @sc_before, @sc_after, @sc_before_save);

    # check if we need to remove the configuration first
    if ($opt_c) {
        # we may remove configuration first
        if ($opt_n) {
            log_cmd("no $cmd\n");
            my_exp("\cuno $cmd\n\cu<!>", '<!>');
            if ($opt_2) {
                log_cmd("no $cmd\n");
                my_exp("\cuno $cmd\n\cu<!>", '<!>');
            }
        }
        if ($opt_V) {
            @sc_before = get_show_config();
            if ($opt_a) {
                @sc_before_save = @sc_before;
            }
        }
    }

    # log the command
    log_cmd("$cmd\n");

    # execute the command
    @res = my_exp("\cu$cmd\n\cu<!>", '<!>');
    if ($res[0] != 1) {
        # command was not accepted
        die "\ncommand not accepted: $cmd\n";
    }

    # check that the command worked
    my $failed = 0;
    if ($res[3] =~ /ERROR:/) {
        $failed = 1;
    }

    # verify that show config contains the new command
    if ($opt_V && !$failed) {
        @sc_after = get_show_config();
        if (scalar(@sc_before) == scalar(@sc_after)) {
            if ($cmd ne 'context local') {
                # no change, which is bad
                die "\nconfig did not change after command was added: $cmd\n";
            }
        } else {
            # go through both configs until we find the new line
            while (scalar(@sc_before) > 0) {
                my $before = shift(@sc_before);
                my $after  = shift(@sc_after);
                next if $before eq $after;
                unshift(@sc_after, $after);
                last;
            }
            my $after = shift(@sc_after);
            $after =~ s/^\s+//;
            if ($cmd ne $after &&
                !($cmd =~ /^\s*password /) &&
                !($after =~ /^\s*password encrypted /)) {
                my $tcmd = " $cmd ";
                $after = " $after ";
                my @words = split(/\s+/, $cmd);
                my $word;
                foreach $word (@words) {
                    $tcmd =~ s/ $word / /;
                    unless ($after =~ / $word /) {
                        die "\nshow config output differs from command: $cmd\n";
                    }
                    $after =~ s/ $word / /;
                }
                if ($after ne ' ') {
                    die "\nshow config output differs from command: $cmd\n";
                }
            }
        }
    }

    # check that the command worked
    if ($failed) {
        # the command didn't work
        if ($opt_c && !$opt_n && !$opt_N) {
            # try the 'no' prefix
            log_cmd("no $cmd\n");
            my_exp("\cuno $cmd\n\cu<!>", '<!>');
            if ($opt_2) {
                log_cmd("$cmd\n");
                my_exp("\cuno $cmd\n\cu<!>", '<!>');
            }
            @res = my_exp("\cu$cmd\n\cu<!>", '<!>');
            if ($res[0] != 1) {
                # command was not accepted
                die "\ncommand not accepted: $cmd\n";
            }
            if ($res[3] =~ /ERROR:/) {
                $failed = 1;
            } else {
                $failed = 0;
            }
        }
    }

    # track any mode change
    my $mode_change = undef;
    if ($opt_c && !$failed) {
        $res[3] =~ /\(cfg\-(\d+)\)#/;
        my $cur_mode = $1;
        if ($mode != $cur_mode) {
            if (defined($$hist{"mode_cmds"})) {
                $$hist{'mode_cmds'} .= "__$cmd";
            } else {
                $$hist{'mode_cmds'} = $cmd;
            }
            $mode_change = $cur_mode;
        }
    }

    # see if we need to re-enter the command and check for silence
    if ($opt_r && !$failed) {
        if ($mode_change) {
            log_cmd("exit\n");
            my_exp("\cuexit\n\cu<!>", '<!>');
        }
        @res = my_exp("\cu$cmd\n\cu<!>", '<!>');
        if ($res[0] != 1) {
            # command was not accepted
            die "\ncommand not accepted: $cmd\n";
        }
        if ($res[3] =~ /ERROR:/) {
            die "\nre-entry of a duplicate config command returned error\n";
        }
    }

    # check if we need to remove the command after executing it,
    # and then add it back again
    if ($opt_c && $opt_a && !$failed) {
        if ($mode_change) {
            log_cmd("exit\n");
            my_exp("\cuexit\n\cu<!>", '<!>');
        }
        log_cmd("no $cmd\n");
        @res = my_exp("\cuno $cmd\n\cu<!>", '<!>');
        if ($opt_V && $cmd ne 'context local') {
            if ($res[0] != 1) {
                die "\ncommand not accepted: $cmd\n";
            }
            if ($res[3] =~ /ERROR:/) {
                die "\nremoval of configuration command returned error\n";
            }
            @sc_after = get_show_config();
            if (scalar(@sc_before_save) != scalar(@sc_after)) {
                die "\nremoval of configuration command had no effect\n";
            }
        }
        if ($opt_2) {
            log_cmd("no $cmd\n");
            my_exp("\cuno $cmd\n\cu<!>", '<!>');
        }
        # re-execute the command
        log_cmd("$cmd\n");
        my_exp("\cu$cmd\n\cu<!>", '<!>');
    }

    # recurse if we changed modes
    if ($mode_change) {
        proc_cmd_opts("", $mode_change, $hist);
    }
}

sub log_cmd($)
{
    my ($cmd) = @_;

    if ($opt_L) {
        print $CmdLog "$cmd";
        $CmdLog->flush;
    }
}

sub my_exp($$)
{
    my ($send_string, $resp_string) = @_;

    if (defined($send_string)) {
        $Exp->send($send_string);
    }
    my @res;
    @res = $Exp->expect($Timeout,
                        "$resp_string",
                        "\cg");
    if (defined($res[1])) {
        if ($res[1] eq '1:TIMEOUT') {
            die "\nTimeout awaiting: $resp_string\n";
        } else {
            die "\nUnexpected expect error: $res[1]\n";
        }
    }
    if ($res[3] =~ /===CLI Terminated===/) {
        die "\nCLI process died\n" unless $res[3] =~ /echo ===/;
    }
    return @res;
}

sub get_cus_vals($)
{
    my ($cmd) = @_;

    my @vals;

    my ($opt, $arg) = split(/__/, $Custom{$cmd}, 2);
    if ($opt eq '_line') {
        my (@lines) = split(/__/, $arg);
        foreach (@lines) {
            s/_/ /g;
            push(@vals, $_);
        }
    } elsif ($opt eq '_arg') {
        my (@args) = split(/::::/, $arg);
        foreach (@args) {
            ($opt, $arg) = split(/:::/, $_);
            my @tmp_vals = get_opt_vals($opt, $arg, undef, undef, undef, undef);
            push(@vals, @tmp_vals);
        }
    } else {
        die "\nUnexpected custom command option: $opt\n";
    }

    return (@vals);
}

sub get_def_vals($$$$$;$$)
{
    my ($opt, $min1, $max1, $min2, $max2, $min3, $max3) = @_;

    my $args = $Default{$opt};
    if (!defined($args)) {
        return ();
    }
    return get_opt_vals($opt, $args, $min1, $max1, $min2, $max2, $min3, $max3);
}

sub get_opt_vals($$$$$$;$$)
{
    my ($opt, $args, $min1, $max1, $min2, $max2, $min3, $max3) = @_;

    if ($opt eq 'decimal-uint') {
        return get_opt_vals_dec_uint($args, $min1, $max1);
    } elsif ($opt eq 'decimal-int') {
        return get_opt_vals_dec_int($args, $min1, $max1);
    } elsif ($opt eq 'hex-uint') {
        return get_opt_vals_hex_uint($args, $min1, $max1);
    } elsif ($opt eq 'ipv4-address') {
        return get_opt_vals_ipv4_addr($args);
    } elsif ($opt eq 'ipv4-mask') {
        return get_opt_vals_ipv4_mask($args);
    } elsif ($opt eq 'ipv4-addr-mask') {
        return get_opt_vals_ipv4_addr_mask($args);
    } elsif ($opt eq 'ipv6-address') {
        return get_opt_vals_ipv6_addr($args);
    } elsif ($opt eq 'ipv6-mask') {
        return get_opt_vals_ipv6_mask($args);
    } elsif ($opt eq 'ipv6-addr-mask') {
        return get_opt_vals_ipv6_addr_mask($args);
    } elsif ($opt eq 'ethernet') {
        return get_opt_vals_ether($args);
    } elsif ($opt eq 'string') {
        return get_opt_vals_string($args, $max1);
    } elsif ($opt eq 'slot') {
        return get_opt_vals_slot($args, $min1, $max1);
    } elsif ($opt eq 'slot-port') {
        return get_opt_vals_slot_port($args, $min1, $max1, $min2, $max2);
    } elsif ($opt eq 'slot-port-chan') {
        return get_opt_vals_slot_port_chan($args, $min1, $max1, $min2, $max2,
                                           $min3, $max3);
    } elsif ($opt eq 'community') {
        return get_opt_vals_comm($args, $min1, $max1, $min2, $max2);
    } else {
        die "\nUnrecognised option: $opt\n";
    }
}

sub get_opt_vals_dec_uint($$$)
{
    my ($args, $min, $max) = @_;

    my $i;
    my %vals;
    my $val;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        if (/^random:([^:]+):([^:\.]+)\.\.(.+)$/) {
            # random set
            my ($count, $low, $high) = ($1, $2, $3);
            $low  = get_val_dec_uint($low, $min, $max);
            $high = get_val_dec_uint($high, $min, $max);
            if ($low > $high) {
                die "\nBad decimal-uint random specification: $_\n";
            }
            foreach $i (1..$count) {
                my $range = $high - $low;
                my $val = int(rand($range)) + $low;
                $val = $val->bstr();
                $vals{$val} = 1;
            }
        } elsif (/\.\./) {
            # range
            my ($first, $last) = split(/\.\./, $_, 2);
            $first = get_val_dec_uint($first, $min, $max);
            $last  = get_val_dec_uint($last, $min, $max);
            if ($first > $last) {
                die "\nBad decimal-uint range specification: $_\n";
            }
            for ($i = $first; $i <= $last; $i++) {
                $val = $i->bstr();
                $vals{$val} = 1;
            }
        } else {
            # single value
            $val = get_val_dec_uint($_, $min, $max);
            $val = $val->bstr();
            $vals{$val} = 1;
        }
    }

    return (keys %vals);
}

sub get_val_dec_uint($$$)
{
    my ($arg, $min, $max) = @_;

    my $mod     = 0;
    my $mod_neg = 0;
    if ($arg =~ /\([\-\+]?\d+\)/) {
        $arg =~ s/\(([\-\+]?)(\d+)\)//;
        my $sign;
        ($sign, $mod) = ($1, $2);
        if (defined($sign)) {
            if ($sign eq '-') {
                $mod_neg = 1;
            }
        }
        $mod = Math::BigInt->new($mod);
    }
    if ($arg =~ /^max$/) {
        $arg = $DecUintMax;
    } elsif ($arg =~ /^min$/) {
        $arg = 0;
    } else {
        unless ($arg =~ /^\d+$/) {
            die "\nBad decimal-uint argument: $arg\n";
        }
    }
    $arg = Math::BigInt->new($arg);
    if ($mod_neg) {
        $arg = $arg - $mod;
    } else {
        $arg = $arg + $mod;
    }

    if (defined($min) && $arg < $min) {
        $arg = Math::BigInt->new($min);
    }
    if (defined($max) && $arg > $max) {
        $arg = Math::BigInt->new($max);
    }

    return $arg;
}

sub get_opt_vals_dec_int($$$)
{
    my ($args, $min, $max) = @_;

    my $i;
    my %vals;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        if (/^random:([^:]+):([^:\.]+)\.\.(.+)$/) {
            # random set
            my ($count, $low, $high) = ($1, $2, $3);
            $low  = get_val_dec_int($low, $min, $max);
            $high = get_val_dec_int($high, $min, $max);
            if ($low > $high) {
                die "\nBad decimal-int random specification: $_\n";
            }
            foreach $i (1..$count) {
                my $range = $high - $low;
                my $rval = int(rand($range)) + $low;
                $vals{$rval} = 1;
            }
        } elsif (/\.\./) {
            # range
            my ($first, $last) = split(/\.\./, $_, 2);
            $first = get_val_dec_int($first, $min, $max);
            $last  = get_val_dec_int($last, $min, $max);
            if ($first > $last) {
                die "\nBad decimal-int range specification: $_\n";
            }
            for ($i = $first; $i <= $last; $i++) {
                $vals{$i} = 1;
            }
        } else {
            # single value
            my $val = get_val_dec_int($_, $min, $max);
            $vals{$val} = 1;
        }
    }

    return (keys %vals);
}

sub get_val_dec_int($$$)
{
    my ($arg, $min, $max) = @_;

    my $mod     = 0;
    my $mod_neg = 0;
    if ($arg =~ /\([\-\+]?\d+\)/) {
        $arg =~ s/\(([\-\+]?)(\d+)\)//;
        my $sign;
        ($sign, $mod) = ($1, $2);
        if (defined($sign)) {
            if ($sign eq '-') {
                $mod_neg = 1;
            }
        }
    }
    if ($arg =~ /^max$/) {
        $arg = $DecIntMax;
    } elsif ($arg =~ /^min$/) {
        $arg = $DecIntMin;
    } else {
        unless ($arg =~ /^[\-]?\d+$/) {
            die "\nBad decimal-int argument: $arg\n";
        }
    }
    if ($mod_neg) {
        $arg -= $mod;
    } else {
        $arg += $mod;
    }

    if (defined($min) && $arg < $min) {
        $arg = $min;
    }
    if (defined($max) && $arg > $max) {
        $arg = $max;
    }

    return $arg;
}

sub get_opt_vals_hex_uint($$$)
{
    my ($args, $min, $max) = @_;

    if (defined($min)) {
        $min = Math::BigInt->new("0x$min");
    }
    if (defined($max)) {
        $max = Math::BigInt->new("0x$max");
    }
    my $i;
    my %vals;
    my $val;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        if (/^random:([^:]+):([^:\.]+)\.\.(.+)$/) {
            # random set
            my ($count, $low, $high) = ($1, $2, $3);
            $low  = get_val_hex_uint($low, $min, $max);
            $high = get_val_hex_uint($high, $min, $max);
            if ($low > $high) {
                die "\nBad hex-uint random specification: $_\n";
            }
            foreach $i (1..$count) {
                my $range = $high - $low;
                $val = int(rand($range)) + $low;
                $val = $val->as_hex();
                $val =~ s/^0x//;
                $vals{$val} = 1;
            }
        } elsif (/\.\./) {
            # range
            my ($first, $last) = split(/\.\./, $_, 2);
            $first = get_val_hex_uint($first, $min, $max);
            $last  = get_val_hex_uint($last, $min, $max);
            if ($first > $last) {
                die "\nBad hex-uint range specification: $_\n";
            }
            for ($i = $first; $i <= $last; $i++) {
                $val = $i->as_hex();
                $val =~ s/^0x//;
                $vals{$val} = 1;
            }
        } else {
            # single value
            $val = get_val_hex_uint($_, $min, $max);
            $val = $val->as_hex();
            $val =~ s/^0x//;
            $vals{$val} = 1;
        }
    }

    return (keys %vals);
}

sub get_val_hex_uint($$$)
{
    my ($arg, $min, $max) = @_;

    my $mod     = 0;
    my $mod_neg = 0;
    if ($arg =~ /\([\-\+]?[[:xdigit:]]+\)/) {
        $arg =~ s/\(([\-\+]?)([[:xdigit:]]+)\)//;
        my $sign;
        ($sign, $mod) = ($1, $2);
        if (defined($sign)) {
            if ($sign eq '-') {
                $mod_neg = 1;
            }
        }
        $mod = Math::BigInt->new("0x$mod");
    }
    if ($arg =~ /^max$/) {
        $arg = $HexUintMax;
    } elsif ($arg =~ /^min$/) {
        $arg = 0;
    } else {
        unless ($arg =~ /^[[:xdigit:]]+$/) {
            die "\nBad hex-uint argument: $arg\n";
        }
    }
    $arg = Math::BigInt->new("0x$arg");
    if ($mod_neg) {
        $arg = $arg - $mod;
    } else {
        $arg = $arg + $mod;
    }

    if (defined($min) && $arg < $min) {
        $arg = Math::BigInt->new("0x$min");
    }
    if (defined($max) && $arg > $max) {
        $arg = Math::BigInt->new("0x$max");
    }

    return $arg;
}

sub get_opt_vals_ipv4_addr($)
{
    my ($args) = @_;

    my $i;
    my %vals;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        if (/^random:([^:]+):([^:\.]+)\.\.(.+)$/) {
            # random set
            my ($count, $low, $high) = ($1, $2, $3);
            $low  = ipv4_addr_txt2bin($low);
            $high = ipv4_addr_txt2bin($high);
            if ($low > $high) {
                die "\nBad random random specification: $_\n";
            }
            foreach $i (1..$count) {
                my $range = $high - $low;
                if ($range > $DecIntMax) {
                    die "\nUnable to handle ipv4 range (too big): $_\n";
                }
                my $rval = $low + int(rand($range->as_int()));
                $rval = ipv4_addr_bin2txt($rval);
                $vals{$rval} = 1;
            }
        } elsif (/\.\./) {
            # range
            my ($first, $last) = split(/\.\./, $_, 2);
            $first = ipv4_addr_txt2bin($first);
            $last  = ipv4_addr_txt2bin($last);
            if ($first > $last) {
                die "\nBad ipv4-address range specification: $_\n";
            }
            my $addr;
            for ($addr = $first; $addr <= $last; $addr++) {
                my $val = ipv4_addr_bin2txt($addr);
                $vals{$val} = 1;
            }
        } else {
            # single value
            $vals{$_} = 1;
        }
    }

    return (keys %vals);
}

sub ipv4_addr_txt2bin($)
{
    my ($arg) = @_;

    unless ($arg =~ /^[\d\.]+/) {
        die "\nBad ipv4-address: $arg\n";
    }
    if ($arg =~ /^\./ || $arg =~ /\.$/) {
        die "\nBad ipv4-address: $arg\n";
    }
    my @nums = split(/\./, $arg);
    unless (scalar(@nums) == 4) {
        die "\nBad ipv4-address: $arg\n";
    }
    my $num;
    foreach $num (@nums) {
        if ($num < 0 || $num > 255) {
            die "\nBad ipv4-address: $arg\n";
        }
    }
    my $val = Math::BigInt->new("$nums[3]");
    $val += $nums[2] << 8;
    $val += $nums[1] << 16;
    $val += $nums[0] << 24;

    return $val;
}

sub ipv4_addr_bin2txt($)
{
    my ($arg) = @_;

    my @nums;
    $nums[0] = $arg >> 24;
    $nums[1] = ($arg >> 16) & 0xff;
    $nums[2] = ($arg >> 8) & 0xff;
    $nums[3] = $arg & 0xff;
    my $val = $nums[0]->bstr();
    $val .= '.' . $nums[1]->bstr();
    $val .= '.' . $nums[2]->bstr();
    $val .= '.' . $nums[3]->bstr();

    return $val;
}

sub get_opt_vals_ipv4_mask($)
{
    my ($args) = @_;

    my %vals;
    my $i;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        if (/\.\./) {
            # range
            my ($first, $last) = split(/\.\./, $_, 2);
            if ($first > $last) {
                die "\nBad ipv4-mask range specification: $_\n";
            }
            for ($i = $first; $i <= $last; $i++) {
                $vals{$i} = 1;
            }
        } else {
            # single value
            $vals{$_} = 1;
        }
    }

    return (keys %vals);
}

sub get_opt_vals_ipv4_addr_mask($)
{
    my ($args) = @_;

    my %vals;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        unless (/\//) {
            die "\nBad ipv4-addr-mask specification: $_\n";
        }
        my ($addr, $mask) = split(/\//, $_, 2);
        my (@a_vals) = get_opt_vals_ipv4_addr($addr);
        my (@m_vals) = get_opt_vals_ipv4_mask($mask);
        foreach $addr (@a_vals) {
            foreach $mask (@a_vals) {
                $vals{"$addr/$mask"} = 1;
            }
        }
    }

    return (keys %vals);
}

sub get_opt_vals_ipv6_addr($)
{
    my ($args) = @_;

    my (@vals) = split(/\,/, $args);

    return (@vals);
}

sub get_opt_vals_ipv6_mask($)
{
    my ($args) = @_;

    my %vals;
    my $i;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        if (/\.\./) {
            # range
            my ($first, $last) = split(/\.\./, $_, 2);
            if ($first > $last) {
                die "\nBad ipv6-mask range specification: $_\n";
            }
            for ($i = $first; $i <= $last; $i++) {
                $vals{$i} = 1;
            }
        } else {
            # single value
            $vals{$_} = 1;
        }
    }

    return (keys %vals);
}

sub get_opt_vals_ipv6_addr_mask($)
{
    my ($args) = @_;

    my (@vals) = split(/\,/, $args);

    return (@vals);
}

sub get_opt_vals_ether($)
{
    my ($args) = @_;

    my (@vals) = split(/\,/, $args);

    return (@vals);
}

sub get_opt_vals_string($$)
{
    my ($args, $max) = @_;

    my (@vals);
    my (@v) = split(/\,/, $args);
    foreach (@v) {
        if (/\*/ && ~/^\*$/) {
            my ($str, $rep) = split(/\*/, $_, 2);
            unless ($rep =~ /^\d+$/) {
                die "\nBad string specification: $_\n";
            }
            $str = $str x $rep;
            if (!defined($max) || $max > $StrLenMax) {
                $max = $StrLenMax;
            }
            if (length($str) > $max) {
                $str = substr($str, 0, $max);
            }
            push(@vals, $str);
        } else {
            push(@vals, $_);
        }
    }

    return (@vals);
}

sub get_min_max_val($$$)
{
    my ($val, $min, $max) = @_;

    if ($val < $min) {
        $val = $min;
    }
    if ($val > $max) {
        $val = $max;
    }
    return $val;
}

sub get_opt_vals_slot($$$)
{
    my ($args, $min, $max) = @_;

    my %vals;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        my ($slot_from, $slot_to);
        if (/^(\d+)\.\.(\d+)$/) {
            ($slot_from, $slot_to) = ($1, $2);
        } elsif (/^(\d+)$/) {
            $slot_to   = $1;
            $slot_from = $1;
        } else {
            die "\nBad slot specification: $_\n";
        }
        $slot_to = get_min_max_val($slot_to, $min, $max);
        $slot_from = get_min_max_val($slot_from, $min, $max);
        my $slot;
        for ($slot = $slot_from; $slot <= $slot_to; $slot++) {
            $vals{$slot} = 1;
        }
    }

    return (keys %vals);
}

sub get_opt_vals_slot_port($$$$$)
{
    my ($args, $min1, $max1, $min2, $max2) = @_;

    my %vals;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        unless (/\//) {
            die "\nBad slot-port specification: $_\n";
        }
        my ($slot, $port) = split(/\//, $_);
        my ($slot_from, $slot_to, $port_from, $port_to);
        if ($slot =~ /^(\d+)\.\.(\d+)$/) {
            ($slot_from, $slot_to) = ($1, $2);
        } elsif ($slot =~ /^\d+$/) {
            $slot_to   = $slot;
            $slot_from = $slot;
        } else {
            die "\n Bad slot-port (slot) specification: $slot\n";
        }
        $slot_to = get_min_max_val($slot_to, $min1, $max1);
        $slot_from = get_min_max_val($slot_from, $min1, $max1);
        if ($port =~ /^(\d+)\.\.(\d+)$/) {
            ($port_from, $port_to) = ($1, $2);
        } elsif ($port =~ /^\d+$/) {
            $port_to   = $port;
            $port_from = $port;
        } else {
            die "\nBad slot-port (port) specification: $port\n";
        }
        $port_to = get_min_max_val($port_to, $min2, $max2);
        $port_from = get_min_max_val($port_from, $min2, $max2);
        for ($slot = $slot_from; $slot <= $slot_to; $slot++) {
            for ($port = $port_from; $port <= $port_to; $port++) {
                $vals{"$slot/$port"} = 1;
            }
        }
    }

    return (keys %vals);
}

sub get_opt_vals_slot_port_chan($$$$$$$)
{
    my ($args, $min1, $max1, $min2, $max2, $min3, $max3) = @_;

    my %vals;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        unless (/\/.*\//) {
            die "\nBad slot-port-chan specification: $_\n";
        }
        my ($slot, $port, $chan) = split(/\//, $_);
        my ($slot_from, $slot_to, $port_from, $port_to, $chan_from, $chan_to);
        if ($slot =~ /^(\d+)\.\.(\d+)$/) {
            ($slot_from, $slot_to) = ($1, $2);
        } elsif ($slot =~ /^\d+$/) {
            $slot_to   = $slot;
            $slot_from = $slot;
        } else {
            die "\n Bad slot-port-chan (slot) specification: $slot\n";
        }
        $slot_to = get_min_max_val($slot_to, $min1, $max1);
        $slot_from = get_min_max_val($slot_from, $min1, $max1);
        if ($port =~ /^(\d+)\.\.(\d+)$/) {
            ($port_from, $port_to) = ($1, $2);
        } elsif ($port =~ /^\d+$/) {
            $port_to   = $port;
            $port_from = $port;
        } else {
            die "\nBad slot-port-chan (port) specification: $port\n";
        }
        $port_to = get_min_max_val($port_to, $min2, $max2);
        $port_from = get_min_max_val($port_from, $min2, $max2);
        if ($chan =~ /^(\d+)\.\.(\d+)$/) {
            ($chan_from, $chan_to) = ($1, $2);
        } elsif ($chan =~ /^\d+$/) {
            $chan_to   = $chan;
            $chan_from = $chan;
        } else {
            die "\nBad slot-port-chan (chan) specification: $port\n";
        }
        $chan_to = get_min_max_val($chan_to, $min3, $max3);
        $chan_from = get_min_max_val($chan_from, $min3, $max3);
        for ($slot = $slot_from; $slot <= $slot_to; $slot++) {
            for ($port = $port_from; $port <= $port_to; $port++) {
                for ($chan = $chan_from; $chan <= $chan_to; $chan++) {
                    $vals{"$slot/$port/$chan"} = 1;
                }
            }
        }
    }

    return (keys %vals);
}

sub get_opt_vals_comm($$$$$)
{
    my ($args, $min1, $max1, $min2, $max2) = @_;

    my $i;
    my %vals;
    my (@arg) = split(/\,/, $args);
    foreach (@arg) {
        unless (/:/) {
            die "\nBad community specification: $_\n";
        }
        my ($num1, $num2) = split(/:/, $_, 2);
        my ($low1, $high1) = get_val_comm_low_high($num1, $min1, $max1);
        my ($low2, $high2) = get_val_comm_low_high($num2, $min2, $max2);
        foreach $num1 ($low1..$high1) {
            foreach $num2 ($low2..$high2) {
                $vals{"$num1:$num2"} = 1;
            }
        }
    }

    return (keys %vals);
}

sub get_val_comm_low_high($$$)
{
    my ($arg, $min, $max) = @_;

    my ($low, $high);
    if ($arg =~ /\.\./) {
        # range
        ($low, $high) = split(/\.\./, $arg, 2);
        $low  = get_val_comm($low, $min, $max);
        $high = get_val_comm($high, $min, $max);
        if ($low > $high) {
            die "\nBad community range specification: $arg\n";
        }
    } else {
        # single value
        $low = get_val_comm($arg, $min, $max);
        $high = $low;
    }

    return ($low, $high);
}

sub get_val_comm($$$)
{
    my ($arg, $min, $max) = @_;

    my $mod     = 0;
    my $mod_neg = 0;
    if ($arg =~ /\([\-\+]?\d+\)/) {
        $arg =~ s/\(([\-\+]?)(\d+)\)//;
        my $sign;
        ($sign, $mod) = ($1, $2);
        if (defined($sign)) {
            if ($sign eq '-') {
                $mod_neg = 1;
            }
        }
    }
    if ($arg =~ /^max$/) {
        $arg = $CommMax;
    } elsif ($arg =~ /^min$/) {
        $arg = 0;
    } else {
        unless ($arg =~ /^\d+$/) {
            die "\nBad community argument: $arg\n";
        }
    }
    if ($mod_neg) {
        $arg -= $mod;
    } else {
        $arg += $mod;
    }

    if (defined($min) && $arg < $min) {
        $arg = $min;
    }
    if (defined($max) && $arg > $max) {
        $arg = $max;
    }

    return $arg;
}

#!/usr/bin/python2.6

import os
import numpy
import Gnuplot
import subprocess
import datetime

REPORT_DIR ='result'
REPORT_TIME = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

def scp_report(vector):
	report = './{0}/{1}-{2}.csv'.format(REPORT_DIR, vector, REPORT_TIME)
	if not os.path.isdir("./" + REPORT_DIR + "/"):
		os.mkdir("./" + REPORT_DIR + "/")
	return report

def scp_plot(vector, report):
	proc = subprocess.Popen(['gnuplot','-p'],
        	                shell=True,
                	        stdin=subprocess.PIPE,
                        	)
	proc.stdin.write('set terminal png size 700,550\n')
	proc.stdin.write('set output "./{0}/{1}-{2}-distribution-chart.png"\n'.format(REPORT_DIR, vector, REPORT_TIME))
	proc.stdin.write('set boxwidth 0.05 absolute\n')
	proc.stdin.write('set grid\n')
	proc.stdin.write('set key inside left top vertical Right noreverse enhanced autotitles nobox\n')
	proc.stdin.write('set xzeroaxis linetype 0 linewidth 1.000\n')
	proc.stdin.write('set yzeroaxis linetype 0 linewidth 1.000\n')
	proc.stdin.write('set zzeroaxis linetype 0 linewidth 1.000\n')
	proc.stdin.write('bin(x, s) = s*int(x/s)\n')
	proc.stdin.write('GPFUN_bin = "bin(x, s) = s*int(x/s)"\n')
	proc.stdin.write('plot "{0}" u 1:(0.25*rand(0)-.35) t "",      "" u (bin($1,0.05)):(20/300.) s f t "frequency distribution" w boxes,      "" u 1:(1/300.) s cumul t "cumulative distribution"\n'.format(report))
	proc.stdin.write('quit\n')
	proc.stdin.close()

if __name__ == "__main__":
	v = numpy.random.normal(3,1,1000)
	report = scp_report('cash')
	numpy.savetxt(report,v)
	scp_plot('cash', report)



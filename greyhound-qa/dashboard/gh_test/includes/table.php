<?php

/**
* Framework to generate styled table markup
* @author Saurabh Odhyan (sodhyan@zynga.com)
*/

class TableMarkup {

	private static function get_table_class($class) {
		if($class == "row1") {
			return "row2";
		} else {
			return "row1";
		}
	}

	/**
	* Get markup for the table header
	* @method get_head_markup
	* @private
	*/
	private static function get_head_markup($tblStruct, $tblData) {
		$markup = "<tr>";
		for($i = 0; $i < sizeof($tblStruct); $i++) {
			$label = $tblStruct[$i]["label"];
			$markup .= "<td class=hd>$label</td>";
		}
		$markup .= "</tr>";
		return $markup;
	}


	/**
	* Get markup for the table body
	* @method get_body_markup
	* @private
	*/
	private static function get_body_markup($tblStruct, $tblData) {
		$markup = "";
		$class = "row2";
		for($r = 0; $r < sizeof($tblData); $r++) {
			$row = $tblData[$r];
			$class = self::get_table_class($class);
            $markup .= "<tr class=$class>";
			for($c = 0; $c < sizeof($row); $c++) {
				$col = $row[$c];

				if(isset($tblStruct[$c]["minmax"])) {
					$minmax = $tblStruct[$c]["minmax"];
				} else {
					$minmax = 0;
				}

				if(isset($tblStruct[$c]["align"])) {
					$align = $tblStruct[$c]["align"];
				} else {
					$align = "left";
				}
				$markup .= "<td class=$align>";

				if(isset($tblStruct[$c]["bold"]) && $tblStruct[$c]["bold"] == 1) {
					$markup .= "<b>$col</b>";
				} else {
					$markup .= $col;
				}

				$markup .= "</td>";
			}
			$markup .= "</tr>";
		}
		return $markup;
	}


	/**
	* Get markup for the table
	* @method get_table_markup
	* @public
	*
	* @param $tblStruct Structure of the table being constructed
    *
    * Format:
    *   {
    *       [0] => {
    *           "label" => "page",
    *           "align" => "left/center/right",
    *           "bold" => 0/1,
    *       },
    *       [1] => {
    *           ...
    *       },
    *       ...
    *   }
	*
	* @param $tblData Data for the table being constructed
    *
    * 2D Array where element at each index represent the data 
    * to be displayed in the table at that index
    *
    * Header labels are taken care of by $tblStruct
    *
    * Example:
    *
    * x1, x2, x3
    * y1, y2, y3
    * z1, z2, z3
	*/
	public static function get_table_markup($tblStruct, $tblData) {
		$markup = "<div class='misty-table'>";
		$markup .= "<table cellspacing=0 cellpadding=0>";

		$markup .= self::get_head_markup($tblStruct, $tblData);
		$markup .= self::get_body_markup($tblStruct, $tblData);

		$markup .= "</table>";
		$markup .= "</div>";

		return $markup;
	}
}

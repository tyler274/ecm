/*************************
 * "Members" table setup *
 *************************/
/**
 * Needs three global constants to be defined:
 *      - DIRECTOR_ACCESS_LVL
 *      - COLOR_THRESHOLDS
 *      - AJAX_URL
 **/

SHOW_SHIPS = 'all';

function membersRowCallback( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
    /* apply color to all access level cells */
    accessLvl = aData[3];
    if (accessLvl == DIRECTOR_ACCESS_LVL) {
        $('td:eq(3)', nRow).html('<b>DIRECTOR</b>');
    }
    $('td:eq(3)', nRow).addClass("row-" + getAccessColor(accessLvl, COLOR_THRESHOLDS));

    /* hide titles column */
    $('td:eq(8)', nRow).hide()

    /* set titles tooltip on each row */
    titles = aData[7]
    if (titles != "") {
        $('td:eq(3)', nRow).attr("title", titles)
        $('td:eq(3)', nRow).cluetip({
            splitTitle: '|',
            dropShadow: false,
            cluetipClass: 'jtip',
            positionBy: 'mouse',
            tracking: true
        });
    }

    return nRow;
}
        
function membersServerParams( aoData ) {
    /* Add some extra variables to the url */
	if ($('#ships_selector button').length) {
		aoData.push( {
			name: 'show_ships',
			value: SHOW_SHIPS,
		});
	}
	if ($('#corp_selector').length) {
		aoData.push({
			name: 'corp',
			value: $('#corp_selector').val(),
		});
	}
}
        
function membersStateSaveParams (oSettings, oData) {
    oData.sFilter = $("#search_text").val();
    if ($('#ships_selector button').length) {
    	oData.show_ships = SHOW_SHIPS;
    }
    if ($('#corp_selector').length) {
    	oData.corp = $('#corp_selector').val();
    }
}

function membersStateLoadParams (oSettings, oData) {
    $("#search_text").val(oData.sFilter);
    if ('show_ships' in oData) {
    	var buttons = $('#ships_selector button');
    	SHOW_SHIPS = oData.show_ships;
        if (buttons[0].id == SHOW_SHIPS) {
            $(buttons[0]).attr('aria-pressed', 'true');
            $(buttons[1]).attr('aria-pressed', 'false');
        } else {
            $(buttons[0]).attr('aria-pressed', 'true');
            $(buttons[1]).attr('aria-pressed', 'false');
        }
    }
    if ('corp' in oData) {
    	$('#corp_selector').val(oData.corp);
    }
    return true;
}
        
$(document).ready(function () {
    $('#ships_selector button').on('click', function (event) {
    	event.preventDefault();
    	SHOW_SHIPS = this.id;
    	$('#members_table').dataTable().fnDraw();
        if ($('#all').id == SHOW_SHIPS) {
            $('#all').attr('aria-pressed', 'true');
            $('#supers').attr('aria-pressed', 'false');
        } else {
            $('#supers').attr('aria-pressed', 'true');
            $('#all').attr('aria-pressed', 'false');
        }
	});
    
    $('#corp_selector').on('change', function () {
    	$('#members_table').dataTable().fnDraw();
    });
});


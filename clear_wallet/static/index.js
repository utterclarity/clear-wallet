function flash(msg, category) {
    var num = window.clear_wallet.last_err++;
    category = category || "success";
    //<p class="flash flash-{{ category }} flash-num-{{ loop.index }}">{{ message }}</p>
    $err = $('<p class="flash flash-' + category + ' flash-num-' + num + '">' + msg + '</p>');
    $('#flashes').append($err);
    setTimeout(function () {
        $err.slideUp("slow", function() {
            $err.remove();
        });
    }, 1000 * 2);
}

function pull_data() {
    $('#spinner').slideDown();
    $.get('/data.json', function (data) {
        if (data == null || data.coins == null || data.transactions == null) {
            flash(
                "Something went wrong querying the server.<br>"
                + "Retry by pressing the red <b>RETRY</b> button.",
                "error"
            );
            $('#spinner').slideUp();
            $('#retry-query').slideDown();
            return;
        }
        $('#block-address .my-addr').text(data.coins.addr);
        $('#block-address .my-coins').text(data.coins.amount);
        $('#block-transactions-body').empty();
        for (var i = data.transactions.transactions.length - 1; i >= 0; i--) {
            var d = data.transactions.transactions[i];
            var $tr = $('<tr/>');
            var $me_span = $('<b/>').append($('<span title="click to copy" class="my-addr">You</span>'));
            $me_span.click(my_addr_hook);
            if (d.to == window.clear_wallet.addr) {
                $tr.append($('<td/>').append($me_span));
            } else {
                $tr.append($('<td/>').html(d.to));
            }
            if (d.from == window.clear_wallet.addr) {
                $tr.append($('<td/>').append($me_span));
            } else {
                $tr.append($('<td/>').html(d.from));
            }
            $tr.append($('<td/>').html(d.amount));
            $('#block-transactions-body').append($tr);
        };
        $('#spinner').slideUp();
    });
}

window.clear_wallet = window.clear_wallet || {};
window.clear_wallet.last_id = 0;
window.clear_wallet.last_err = 0;
window.clear_wallet.is_main_page = false;

function my_addr_hook() {
    prompt("Here is your address: (Ctrl-C to copy)", window.clear_wallet.addr);
}

$(document).ready(function() {
	if (!window.clear_wallet.is_main_page) {
		return;
	}
	$('#download-stamp').click(function () {
		window.location = "/bloostamp/get";
	});
    $('#retry-query').click(function () {
        $(this).slideUp();
        pull_data();
    });
    $('#refresh-query').click(function () {
    	pull_data();
    });
    $(".my-addr").click(my_addr_hook);

    pull_data();
});
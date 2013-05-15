function flash(msg, category) {
	var num = window.clear_wallet.last_err++;
	category = category || "success";
	//<p class="flash flash-{{ category }} flash-num-{{ loop.index }}">{{ message }}</p>
	$err = $('<p class="flash flash-' + category + ' flash-num-' + num + '">' + msg + '</p>');
	$('#flashes').append($err);
	setTimeout(function() {
		$err.slideUp("slow", function() {
			$err.remove();
		});
	}, 1000 * 2);
}

function pull_data() {
	$('#spinner').slideDown();
	$.get('/data.json', function (data) {
		$('#block-address .my-addr').text(data.coins.addr);
		$('#block-address .my-coins').text(data.coins.amount);
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

function my_addr_hook() {
	prompt("Here is your address: (Ctrl-C to copy)", window.clear_wallet.addr);
}

$(document).ready(function() {
	$("#test-spinner").click(function () {
		$('#spinner').slideDown();
		setTimeout(function () {$('#spinner').slideUp();}, 2000);
	});
	$(".my-addr").click(my_addr_hook);
	pull_data();
});
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

function refresh_captcha() {
	Recaptcha.create(window.recaptcha_public_key,
		"recaptcha-goes-here",
		{
			theme: "clean",
			callback: function() {}
		}
	);
}

window.clear_wallet = window.clear_wallet.addr || {};
window.clear_wallet.last_id = 0;
window.clear_wallet.last_err = 0;

$(document).ready(function() {
	$(".my-addr").click(function () {
		prompt("Here is your address: (Ctrl-C to copy)", window.clear_wallet.addr);
	});
});
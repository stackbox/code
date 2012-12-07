/* from http://trevordavis.net/blog/tutorial/jquery-inline-form-labels/ */
$(document).ready(function() {
	$('input[title]').each(function() {
		if($(this).val() === '') {
			$(this).val($(this).attr('title'));
			/* MJA extra code to allow for a different text color when showing inline labels */
			$(this).addClass('inline-label');
		}

		$(this).focus(function() {
			if($(this).val() === $(this).attr('title')) {
				$(this).val('').addClass('focused');
				$(this).removeClass('inline-label');
			}
		});

		$(this).blur(function() {
			if($(this).val() === '') {
				$(this).val($(this).attr('title')).removeClass('focused');
				$(this).addClass('inline-label');
			}
		});
	});
});

/* from o'reilly jquery cookbook chapter 13 */
/* we should rework this to a proper plug-in */

function init_tooltip() {

  // Does element exist?
  if (!$('.tooltip').length) {

    // If not, exit.
    return;
  }

  // Insert tool tip (hidden).
  $('body').append('<div id="tooltip_outer"><div id="tooltip_inner"></div></div>');

  // Empty variables.
  var $tt_title, $tt_alt;

  var $tt = $('#tooltip_outer');
  var $tt_i = $('#tooltip_inner');

  // Watch for hover.
  $('.tooltip').hover(function() {

    // Store title, empty it.
    if ($(this).attr('title')) {
      $tt_title = $(this).attr('title');
      $(this).attr('title', '');
    }

    // Store alt, empty it.
    if ($(this).attr('alt')) {
      $tt_alt = $(this).attr('alt');
      $(this).attr('alt', '');
    }

    // Insert text.
    $tt_i.html($tt_title);

    // Show tool tip.
    $tt.show();
  },
  function() {

    // Hide tool tip.
    $tt.hide();

    // Empty text.
    $tt_i.html('');

    // Fix title.
    if ($tt_title) {
      $(this).attr('title', $tt_title);
    }

    // Fix alt.
    if ($tt_alt) {
      $(this).attr('alt', $tt_alt);
    }

  // Watch for movement.
  }).mousemove(function(ev) {

    // Event coordinates.
    var $ev_x = ev.pageX;
    var $ev_y = ev.pageY;

    // Tool tip coordinates.
    var $tt_x = $tt.outerWidth();
    var $tt_y = $tt.outerHeight();

    // Body coordinates.
    var $bd_x = $('body').outerWidth();
    var $bd_y = $('body').outerHeight();

    // Move tool tip.
    $tt.css({
      'top': $ev_y + $tt_y > $bd_y ? $ev_y - $tt_y : $ev_y,
      'left': $ev_x + $tt_x + 20 > $bd_x ? $ev_x - $tt_x - 10 : $ev_x + 15
    });
  });
}

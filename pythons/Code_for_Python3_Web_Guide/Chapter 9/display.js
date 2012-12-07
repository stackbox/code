var v=$(".mb-textarea").val();
var n=$(".mb-textarea").attr('name');
$(".mb-textarea").wrap('<div id="mb-placeholder" />').remove();
var i=$('<textarea cols="40" rows="10" />');
i.val(v);

i.attr('name',n);
i.addClass("mb-textarea");
$("#mb-placeholder").append(i);

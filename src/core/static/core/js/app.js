$(function () {
  $('[data-toggle="tooltip"]').tooltip({
    container: 'body',
    html: true,
    template: '<div class="tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner text-left"></div></div>'
  })
})

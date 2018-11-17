window.Popper = require('popper.js').default;
window.$ = require('jquery');
require('bootstrap');

$('.onClickSubmitDeleteRequest').on('click', (ev) => {
    const $target = $(ev.currentTarget);
    $target.parent().parent().find('form').submit();
});

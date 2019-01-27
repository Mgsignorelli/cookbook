window.Popper = require('popper.js').default;
window.$ = require('jquery');
require('bootstrap');
require('select2');

$('.onClickSubmitDeleteRequest').on('click', (ev) => {
    const $target = $(ev.currentTarget);
    $target.parent().parent().find('form').submit();
});

$('.select2').each(function (index, el) {
    el = $(el);
    el.select2({
        tags: el.data('tags') === 'true',
    });
});

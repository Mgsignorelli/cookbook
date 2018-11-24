let mix = require('laravel-mix');


mix.js('assets/js/app.js', 'public/assets')
  .sass('assets/scss/app.scss', 'public/assets/app.css')
  .copy('assets/images', 'public/images');

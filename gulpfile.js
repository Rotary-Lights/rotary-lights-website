const gulp = require('gulp');
const merge = require('merge-stream');

// Paths to various files
const paths = {
  chartjs: {
    src: 'node_modules/chart.js/dist/*',
    dest: 'rotary_lights_website/static/chartjs/',
  },
  bootstrapIcons: {
    css: 'node_modules/bootstrap-icons/font/bootstrap-icons.min.css',
    fonts: 'node_modules/bootstrap-icons/font/fonts/*',
    destCSS: 'rotary_lights_website/static/bootstrap-icons/css/',
    destFonts: 'rotary_lights_website/static/bootstrap-icons/css/fonts/',
  },
};

// Task for copying Chart.js files
function chartjs() {
  return gulp.src(paths.chartjs.src).pipe(gulp.dest(paths.chartjs.dest));
}

// Task for copying Bootstrap Icons CSS and font files
function bootstrapIcons() {
  // Copy Bootstrap Icons CSS
  const copyCSS = gulp
    .src(paths.bootstrapIcons.css)
    .pipe(gulp.dest(paths.bootstrapIcons.destCSS));

  // Copy Bootstrap Icons font files
  const copyFonts = gulp
    .src(paths.bootstrapIcons.fonts)
    .pipe(gulp.dest(paths.bootstrapIcons.destFonts));

  return merge(copyCSS, copyFonts);
}

// Gulp task to copy all frontend libraries
exports.default = gulp.parallel(chartjs, bootstrapIcons);
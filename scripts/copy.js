'use strict';

var separator = '/';
if (process.platform === 'win32') {
  separator = '\\';
}

var gulp = require('gulp-help')(require('gulp'));
var config = require('..' + separator + 'build.conf');
var path = require('path');

gulp.task('copy', 'Copy the electron files', function() {
  return gulp
    .src(config.paths.electronrequiredfiles, {base: "."})
    .pipe(gulp.dest(function(file) {
      // Doing a bunch of chopping up of the paths to get it to copy
      // into the dist dir correctly
      // First get the directory one up from scripts dir
      var parentPath = __dirname.split(separator);
      parentPath.pop();
      parentPath = parentPath.join(separator);
      // Now lets get rid of everything up to where the assets are
      var filePath = file.path.split(parentPath)[1];
      // Git rid of the filename from the path
      var splitPath = filePath.split(separator);
      filePath = splitPath.slice(2).join(separator);
      filePath = filePath.substring(0, filePath.lastIndexOf(separator));
      // Now override the filepath to only be the name
      file.path = path.basename(file.path);
      // Return back the Path we chopped up above
      return  'dist' + separator + filePath;
    }));
});

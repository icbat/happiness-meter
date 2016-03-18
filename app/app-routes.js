(function () {
  'use strict';

  angular
    .module('mot')
    .config(config);

  function config($urlRouterProvider) {
    $urlRouterProvider.otherwise('/home');
  }
}());

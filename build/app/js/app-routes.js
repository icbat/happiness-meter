(function () {
  'use strict';

  angular
    .module('mot')
    .config(config);

  function config($urlRouterProvider) {
    $urlRouterProvider.otherwise('/home');
  }
}());

//# sourceMappingURL=app-routes.js.map

// http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

angular
    .module('myApp', ['ngRoute', 'ngCookies','ng.confirmField'])
    .config(config)
    .run(run);
config.$inject = ['$routeProvider', '$locationProvider'];
function config($routeProvider, $locationProvider) {
    $routeProvider.when('/',{
        templateUrl: 'view/main.html',
        controller:'homeController',
        controllerAs: 'vm'
    })

    .when('/login',{
        templateUrl: 'view/login.html',
        controller: 'loginController',
        controllerAs: 'vm'
    })

    .when('/signup',{
        templateUrl: 'view/signup.html',
        controller: 'registerController',
        controllerAs: 'vm'
    })

    .when('/myposts',{
        templateUrl: 'view/myposts.html',
        controller: 'myPostController',
        controllerAs: 'vm'
    })

    .when('/managefriends',{
        templateUrl: 'view/manageFriends.html',
        controller: 'myFriendController',
        controllerAs: 'vm'
    })

    .when('/manageinfo',{
        templateUrl: 'view/manageInfo.html',
        controller: 'homeController',
        controllerAs: 'vm'
    })

    .when('/friendPost/:id',{
        templateUrl: 'view/friendpost.html',
        controller: 'friendPostController',
        controllerAs: 'vm'
    })

    .otherwise({
        redirectTo:'/'
    });
};

run.$inject = ['$rootScope', '$location', '$cookieStore', '$http'];
function run($rootScope, $location, $cookieStore, $http) {
    // keep user logged in after page refresh
    $rootScope.globals = $cookieStore.get('globals') || {};
    if ($rootScope.globals.currentUser) {
        $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
    }

    $rootScope.$on('$locationChangeStart', function (event, next, current) {
        // redirect to login page if not logged in and trying to access a restricted page
        var restrictedPage = $.inArray($location.path(), ['/login', '/signup']) === -1;
        var loggedIn = $rootScope.globals.currentUser;
        if (restrictedPage && !loggedIn) {
            $location.path('/login');
        }
    });
}

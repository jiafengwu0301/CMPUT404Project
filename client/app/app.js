var app = angular.module('myApp', ['ngRoute'])
    app.config(['$routeProvider', function($routeProvider){
        $routeProvider.when('/',{
            templateUrl: 'view/login.html',
            controller: 'loginController'
        })

        .when('/main',{
            templateUrl: 'view/main.html'


        })

        .when('/managefriends',{
            templateUrl: 'view/manageFriends.html'


        })

        .when('/manageinfo',{
            templateUrl: 'view/manageInfo.html'


        })

        .when('/signup',{
            templateUrl: 'view/signup.html'


        })

        .otherwise({
            redirectTo:'/'
        });
    }]);

    // app.controller('myCtrl', function($scope) {
    //     $scope.username = "";
    //     $scope.password = "";
    // });

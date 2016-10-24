
app.controller('loginController', ['$scope', function($scope) {
    $scope.username = "John";
    $scope.password = "Doe";
}]);

app.controller('signupController', ['$scope', function($scope) {
    $scope.username = "John";
    $scope.password1 = "Doe";
    $scope.password2 = "Doe";
    $scope.email = "123@456.789";

}]);

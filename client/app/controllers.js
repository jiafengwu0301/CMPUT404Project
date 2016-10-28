// http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

//Login Controller
angular
    .module('myApp')
    .controller('LoginController', LoginController);

LoginController.$inject = ['$location', 'AuthenticationService', 'FlashService'];
function LoginController($location, AuthenticationService, FlashService) {
    var vm = this;

    vm.login = login;

    (function initController() {
        // reset login status
        AuthenticationService.ClearCredentials();
    })();

    function login() {
        vm.dataLoading = true;
        AuthenticationService.Login(vm.username, vm.password, function (response) {
            if (response.success) {
                AuthenticationService.SetCredentials(vm.username, vm.password);
                $location.path('/');
            } else {
                FlashService.Error(response.message);
                vm.dataLoading = false;
            }
        });
    };
}


//Sign Up Controller
angular
    .module('myApp')
    .controller('RegisterController', RegisterController);

RegisterController.$inject = ['UserService', '$location', '$rootScope', 'FlashService'];
function RegisterController(UserService, $location, $rootScope, FlashService) {
    var vm = this;

    vm.register = register;

    function register() {
        vm.dataLoading = true;
        UserService.CreateUser(vm.user)
            .then(function (response) {
                if (response.success) {
                    FlashService.Success('Registration successful', true);
                    $location.path('/login');
                } else {
                    FlashService.Error(response.message);
                    vm.dataLoading = false;
                }
            });
    }
}


//Home page Controller
angular
    .module('myApp')
    .controller('HomeController', HomeController);

HomeController.$inject = ['UserService', '$rootScope'];
function HomeController(UserService, $rootScope) {
    var vm = this;

    vm.user = null;
    vm.allUsers = [];
    vm.deleteUser = deleteUser;
    vm.allPosts = [];
    vm.makePost = makePost;
    vm.post = null;

    initController();

    function initController() {
        loadCurrentUser();
        loadAllUsers();
        loadAllPosts();
    }

    function loadCurrentUser() {
        UserService.GetByUsername($rootScope.globals.currentUser.username)
            .then(function (user) {
                vm.user = user;
            });
    }

    function loadAllUsers() {
        vm.allUsers=UserService.GetAllUser();
    }

    function deleteUser(id) {
        UserService.DeleteUser(id)
        .then(function () {
            loadAllUsers();
        });
    }

    function loadAllPosts() {
        vm.allPosts=UserService.GetAllPost();
    }

    function makePost(){
        vm.post.published_date = Date();
        vm.post.author = vm.user;
        UserService.NewPost(vm.post);
    }
}

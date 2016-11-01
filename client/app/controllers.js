// http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

//Login Controller
angular
    .module('myApp')
    .controller('LoginController', LoginController);

LoginController.$inject = ['$location', 'AuthenticationService', 'FlashService','UserService'];
function LoginController($location, AuthenticationService, FlashService, UserService) {
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
                AuthenticationService.SetCredentials(vm.username, vm.password,response.author);
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
        // alert(vm.user);
        UserService.createUser(vm.user)
            .then(function (response) {
                if (response) {
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

HomeController.$inject = ['UserService', '$rootScope','$location','FlashService'];
function HomeController(UserService, $rootScope, $location, FlashService) {
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;

    vm.allPosts = [];
    vm.makePost = makePost;
    vm.post = null;
    initController();

    function initController() {
        loadAllPosts();
    }

    function loadAllPosts() {
        UserService.getAllPost()
            .then(function (allpost) {
                vm.allPosts = allpost;
            });
    }

    function makePost(){
        vm.dataLoading = true;
        UserService.newPost(vm.post)
            .then(function (response) {
                if (response) {
                    FlashService.Success('Post successful', true);
                    $location.path('/main');
                } else {
                    FlashService.Error(response.message);
                    vm.dataLoading = false;
                }
            });
        // loadAllPosts();
        vm.post.text = "";
    }
}

//My post Controller
angular
    .module('myApp')
    .controller('MyPostController', MyPostController);

MyPostController.$inject = ['UserService', '$rootScope'];
function MyPostController(UserService, $rootScope) {
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.myPosts = [];
    vm.deletePost=deletePost;
    vm.edit = null;
    vm.editPost = editPost;

    initController();

    function initController() {
        loadAllMyPost();
    }

    function loadAllMyPost(){
        UserService.getPost(vm.currentAuthor.id)
            .then(function (allpost) {
                vm.myPosts = allpost;
            });
    }

    function deletePost(id){
        UserService.deletePost(id);
        loadAllMyPost();
    }

    function editPost(id){
        UserService.editPost(id, vm.edit);
        loadAllMyPost();
    }
}

// My friend Controller
angular
    .module('myApp')
    .controller('MyFriendController', MyFriendController);

MyFriendController.$inject = ['UserService', '$rootScope'];
function MyFriendController(UserService, $rootScope) {
    var vm = this;

    vm.myFriends = [];
    vm.friend =null;
    // vm.friendPosts=[];
    // vm.loadFriendPost=loadFriendPost;
    vm.currentAuthor = $rootScope.globals.currentUser.author;
    // vm.friend_id = null;
    // loadFriendPost(friend_id);
    initController();

    function initController() {
        loadAllMyFriend();
    }

    function loadAllMyFriend(){
        UserService.getAllMyFriend(vm.currentAuthor.id)
            .then(function (myFriends) {
                vm.myFriends = myFriends.friends;
            });
    }
    // function loadFriendPost(id){
    //     UserService.getFriendPosts(id)
    //         .then(function (friendPosts) {
    //             vm.friendPosts = friendPosts;
    //             alert(vm.friendPosts[0].text);
    //         });
    // }
}

// Friend Post Controller
angular
    .module('myApp')
    .controller('FriendPostController', FriendPostController);

FriendPostController.$inject = ['UserService', '$rootScope', '$routeParams'];
function FriendPostController(UserService, $rootScope, $routeParams) {
    var vm = this;

    vm.friend_id = $routeParams.id;
    vm.friendPosts=[];
    vm.friend = [];

    initController();

    function initController() {
        getFriendPost();
        getFriend();
    }

    function getFriendPost(){
        UserService.getPost(vm.friend_id)
            .then(function (friendPosts) {
                vm.friendPosts = friendPosts;
            });
    }
    function getFriend(){
        UserService.getAuthorById(vm.friend_id)
            .then(function (friend) {
                vm.friend = friend;
            });
    }
}

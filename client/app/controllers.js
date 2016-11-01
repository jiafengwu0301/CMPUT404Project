// http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example


angular
    .module('myApp')
    .controller('loginController', loginController)
    .controller('registerController', registerController)
    .controller('homeController', homeController)
    .controller('myPostController', myPostController)
    .controller('myFriendController', myFriendController)
    .controller('friendPostController', friendPostController);

// Login Controller
function loginController($location, authenticationService, FlashService, userService) {
    var vm = this;
    vm.errorMessage = "";
    vm.login = login;

    (function initController() {
        authenticationService.clearCredentials();
    })();

    function login() {
        authenticationService.login(vm.username, vm.password)
            .then(function(response){
                if (response.status == 200){
                    authenticationService.setCredentials(vm.username, vm.password, response.data.author);
                    $location.path('/');
                } else {
                    alert(response.response.data.non_field_errors);
                }
            }
        );
    }
}

function registerController(userService, $location, $rootScope, FlashService) {
    var vm = this;
    vm.register = register;
    function register() {
        vm.dataLoading = true;
        userService.createUser(vm.user)
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

function homeController(userService, $rootScope, $location, FlashService) {
    var vm = this;
    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.allPosts = [];
    vm.makePost = makePost;
    vm.post = null;
    vm.comment =null;
    vm.makeComment = makeComment;

    initController();

    function initController() {
        loadAllPosts();
    }

    function loadAllPosts() {
        userService.getAllPost()
            .then(function (allpost) {
                vm.allPosts = allpost.results;
            });

    }

    function makePost(){
        vm.dataLoading = true;
        userService.newPost(vm.post)
            .then(function (response) {
                if (response) {
                    FlashService.Success('Post successful', true);
                    $location.path('/main');
                } else {
                    FlashService.Error(response.message);
                    vm.dataLoading = false;
                }
            });
        vm.post.text = "";
    }

    function makeComment(id){
        userService.newComment(id, vm.comment)
            .then(function(response){
                if (response){
                    loadAllMyPost();
                };
            });
    }
}

function myPostController(userService, $rootScope, $location) {
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.myPosts = [];
    vm.deletePost=deletePost;
    vm.edit = null;
    vm.editPost = editPost;
    vm.deleteComment=deleteComment;

    initController();

    function initController() {
        loadAllMyPost();
    }

    function loadAllMyPost(){
        userService.getPost(vm.currentAuthor.id)
            .then(function (allpost) {
                vm.myPosts = allpost.results;
            });
    }

    function deletePost(id){
        userService.deletePost(id)
            .then(function(response){
                if (response){
                    loadAllMyPost();
                }
            });
    }

    function editPost(id){
        userService.editPost(id, vm.edit)
            .then(function(response){
                if (response){
                    loadAllMyPost();
                }
            });
    }

    function deleteComment(id){
        userService.deleteComment(id)
            .then(function(response){
                if (response){
                    loadAllMyPost();
                }
            })
    }

}

function myFriendController(userService, $rootScope) {
    var vm = this;

    vm.myFriends = [];
    vm.friend =null;
    vm.currentAuthor = $rootScope.globals.currentUser.author;
    initController();

    function initController() {
        loadAllMyFriend();
    }

    function loadAllMyFriend(){
        userService.getAllMyFriend(vm.currentAuthor.id)
            .then(function (myFriends) {
                vm.myFriends = myFriends.friends;
            });
    }
}

function friendPostController(userService, $rootScope, $routeParams) {
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
        userService.getPost(vm.friend_id)
            .then(function (friendPosts) {
                vm.friendPosts = friendPosts;
            });
    }
    function getFriend(){
        userService.getAuthorById(vm.friend_id)
            .then(function (friend) {
                vm.friend = friend;
            });
    }
}

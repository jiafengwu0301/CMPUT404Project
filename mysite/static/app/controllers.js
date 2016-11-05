// Reference: http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

// the controllers used for getting and receiving JSON data from view and userService

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

    // perform login and authentication with server, if username and password correct, use setCredentials to save the authdata as cookie
    function login() {
        authenticationService.login(vm.username, vm.password)
            .then(function(response){
                if (response.status == 200){
                    authenticationService.setCredentials(vm.username, vm.password, response.data.author);
                    $location.path('/main');
                } else {
                    alert(response.response.data.non_field_errors);
                }
            }
        );
    }
}

// Sign Up Controller
function registerController(userService, $location, $rootScope, FlashService) {
    var vm = this;

    vm.register = register;

    // create a new account
    function register() {
        vm.dataLoading = true;
        userService.createUser(vm.user)
            .then(function (response) {

                if (response.success) {
                    FlashService.Success('Registration successful', true);
                    $location.path('/login');
                } else {
                    alert("Sign Not Success");
                    FlashService.Error(response.message);
                    vm.dataLoading = false;
                }
            });
    }
}

// Home Page Controller
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

    // load all post current user can see
    function loadAllPosts() {
        userService.getAllPost()
            .then(function (allpost) {
                vm.allPosts = allpost.results;
                alert(JSON.stringify(vm.allPosts));
                $location.path('/');
            });
    }

    // make a new post
    function makePost(){
        alert(JSON.stringify(vm.post));
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

    // make comment for posts that current user can see
    function makeComment(id){
        userService.newComment(id, vm.comment)
            .then(function(response){
                if (response){
                    loadAllMyPost();
                };
            });
    }
}

// My Posts Controller
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

    // load all post current user made
    function loadAllMyPost(){
        userService.getPost(vm.currentAuthor.id)
            .then(function (allpost) {
                vm.myPosts = allpost.results;
            });
    }

    // delete the post that current user owned
    function deletePost(id){
        userService.deletePost(id)
            .then(function(response){
                if (response){
                    loadAllMyPost();
                }
            });
    }

    // edit a post that current user owned
    function editPost(id){
        userService.editPost(id, vm.edit)
            .then(function(response){
                if (response){
                    loadAllMyPost();
                }
            });
    }

    // delete a comment in a post which current user owned
    function deleteComment(id){
        userService.deleteComment(id)
            .then(function(response){
                if (response){
                    loadAllMyPost();
                }
            })
    }
}

// My Friend Controller
function myFriendController(userService, $rootScope) {
    var vm = this;

    vm.myFriends = [];
    vm.friend =null;
    vm.currentAuthor = $rootScope.globals.currentUser.author;

    initController();

    function initController() {
        loadAllMyFriend();
    }

    // load all friends that current user have
    function loadAllMyFriend(){
        userService.getAllMyFriend(vm.currentAuthor.id)
            .then(function (myFriends) {
                vm.myFriends = myFriends.friends;
            });
    }
}

// Friend Posts Controller
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

    // get all posts that current user's friend have
    function getFriendPost(){
        userService.getPost(vm.friend_id)
            .then(function (friendPosts) {
                vm.friendPosts = friendPosts;
            });
    }

    // get the information of current user's friend
    function getFriend(){
        userService.getAuthorById(vm.friend_id)
            .then(function (friend) {
                vm.friend = friend;
            });
    }
}

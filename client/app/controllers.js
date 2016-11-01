// http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

//Login Controller
angular
    .module('myApp')
    .controller('LoginController', LoginController)
    .controller('RegisterController', RegisterController)
    .controller('HomeController', HomeController)
    .controller('MyPostController', MyPostController)
    .controller('MyFriendController', MyFriendController)
    .controller('FriendPostController', FriendPostController);

function LoginController($location, AuthenticationService, FlashService, UserService) {
    var vm = this;
    vm.errorMessage = "";
    vm.login = login;

    (function initController() {
        AuthenticationService.clearCredentials();
    })();

    function login() {
        AuthenticationService.login(vm.username, vm.password)
            .then(function(response){
                if (response.status == 200){
                    AuthenticationService.setCredentials(vm.username, vm.password, response.data);
                    $location.path('/');
                } else {
                    alert(response.response.data.non_field_errors);
                }
            }
        );
    }
}

function RegisterController(UserService, $location, $rootScope, FlashService) {
    var vm = this;
    vm.register = register;
    function register() {
        vm.dataLoading = true;
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

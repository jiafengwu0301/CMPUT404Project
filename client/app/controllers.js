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
        AuthenticationService.SetCredentials(vm.username, vm.password);
        $location.path('/');
        // AuthenticationService.Login(vm.username, vm.password, function (response) {
        //     if (response.success) {
        //         AuthenticationService.SetCredentials(vm.username, vm.password);
        //         $location.path('/');
        //     } else {
        //         FlashService.Error(response.message);
        //         vm.dataLoading = false;
        //     }
        //
        //     // AuthenticationService.SetCredentials(vm.username, vm.password);
        //     // $location.path('/');
        // });
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
        UserService.CreateUser(vm.user)
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

HomeController.$inject = ['UserService', '$rootScope'];
function HomeController(UserService, $rootScope) {
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;

    vm.allPosts = [];
    vm.makePost = makePost;
    // vm.getAuthor = getAuthor;
    vm.author = null;
    vm.post = null;
    initController();

    function initController() {
        loadAllPosts();
    }

    function loadAllPosts() {
        UserService.GetAllPost()
            .then(function (allpost) {
                vm.allPosts = allpost;
            });
    }

    function makePost(){
        UserService.NewPost(vm.post);
        loadAllPosts();
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
        UserService.GetAllMyPost(vm.currentAuthor.id)
            .then(function (allpost) {
                vm.myPosts = allpost;
            });
    }

    function deletePost(id){
        UserService.DeletePost(id);
        loadAllMyPost();
    }

    function editPost(id){
        UserService.EditPost(id, vm.edit);
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
        UserService.GetAllMyFriend(vm.currentAuthor.id)
            .then(function (myFriends) {
                vm.myFriends = myFriends.friends;
            });
    }
    // function loadFriendPost(id){
    //     UserService.GetFriendPosts(id)
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
        UserService.GetAllMyPost(vm.friend_id)
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

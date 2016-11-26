// Reference: http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

// the controllers used for getting and receiving JSON data from view and userService

angular
    .module('myApp')
    .controller('loginController', loginController)
    .controller('registerController', registerController)
    .controller('homeController', homeController)
    .controller('myPostController', myPostController)
    .controller('myFriendController', myFriendController)
    .controller('friendPostController', friendPostController)
    .controller('myInfoController', myInfoController)
    .controller('githubController',githubController)
    .controller('friendRequestController',friendRequestController);

// Login Controller
function loginController($route, $location, authenticationService, FlashService, userService) {
    var vm = this;
    vm.errorMessage = "";
    vm.login = login;

    (function initController() {
        authenticationService.clearCredentials();
    })();

    // perform login and authentication with server, if username and password correct, use setCredentials to save the authdata as cookie
    function login() {
        vm.dataLoading = true;
        authenticationService.login(vm.username, vm.password)
            .then(function(response){
                if (response.status == 200){
                    authenticationService.setCredentials(vm.username, vm.password, response.data.author);
                    $location.path('/');
                } else {
                    alert(response.response.data.non_field_errors);
                    vm.dataLoading = false;
                }
            }
        );
    }
}

// Sign Up Controller
function registerController(userService,$q, $location, $rootScope, FlashService, Upload) {
    var vm = this;

    vm.register = register;

    // create a new account
    function register() {
        vm.dataLoading = true;
        var deferred = $q.defer();
        if (vm.avatar) {
            Upload.upload({
                url: "https://api.cloudinary.com/v1_1/dbodiislg/upload",
                data: {
                    upload_preset: "b1gyt5ss",
                    file: vm.avatar
                },
                headers:{
                    "Authorization": undefined
                }
            }).success(function(data){
                deferred.resolve(data);
                vm.user.avatar = deferred.promise.$$state.value.url;
                userService.createUser(vm.user)
                    .then(function (response) {
                        if (response) {
                            alert("Success Register");
                            $location.path('/login');
                        } else {
                            alert("Sign Not Success");
                            vm.dataLoading = false;
                        }
                    });
                })
        } else {
            userService.createUser(vm.user)
                .then(function (response) {
                    if (response) {
                        alert("Success Register");
                        $location.path('/login');
                    } else {
                        alert("Sign Not Success");
                        vm.dataLoading = false;
                    }
                });
        }
    }
}

// Home Page Controller
function homeController(userService, $q, $route, $rootScope, $location, FlashService, Upload, $interval) {
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.allPosts = [];
    vm.makePost = makePost;
    vm.post = null;
    vm.comment =null;
    vm.makeComment = makeComment;
    vm.allAuthor = [];
    vm.searchArray = null;
    vm.edit = null;
    vm.editPost = editPost;
    vm.deletePost=deletePost;
    vm.deleteComment=deleteComment;
    vm.sendRemoteRequest = sendRemoteRequest;
    vm.request= null;


    initController();

    function initController() {
        loadAllPosts();
        loadAllAuthor();
    }

    // load all post current user can see
    function loadAllPosts() {
        userService.getAllPost()
            .then(function (allpost) {
                vm.allPosts = allpost.posts;
                userService.getRemotePosts()
                    .then(function(remotePosts){
                        for (var i = 0; i < Object.keys(remotePosts.data).length; i++){
                            for (var j = 0; j < Object.values(remotePosts.data)[i].posts.length; j++){
                                vm.allPosts.push(Object.values(remotePosts.data)[i].posts[j]);
                            }
                        }

                    })
                $location.path('/');
            });
    }

    $interval(checkUpdate,1000);
    function checkUpdate(){
        userService.getAllPost()
            .then(function (allpost) {
                var newposts = allpost.posts;
                userService.getRemotePosts()
                    .then(function(remotePosts){
                        for (var i = 0; i < Object.keys(remotePosts.data).length; i++){
                            for (var j = 0; j < Object.values(remotePosts.data)[i].posts.length; j++){
                                newposts.push(Object.values(remotePosts.data)[i].posts[j]);
                            }
                        }
                        var res =angular.equals(newposts,vm.allPosts);
                        if (!res){
                            vm.allPosts = newposts;
                        }
                    })
            });
    }

    // load all author
    function loadAllAuthor(){
        userService.getAllAuthor()
            .then(function (allAuthor) {
                vm.allAuthor = allAuthor.data.results;
            });
    }

    // make a new post
    function makePost(){
        vm.dataLoading = true;
        var deferred = $q.defer();
        if (vm.image) {
            Upload.upload({
                url: "https://api.cloudinary.com/v1_1/dbodiislg/upload",
                data: {
                    upload_preset: "b1gyt5ss",
                    file: vm.image
                },
                headers:{
                    "Authorization": undefined
                }
            }).success(function(data){
                deferred.resolve(data);
                vm.post.image = deferred.promise.$$state.value.url;
                if (vm.post.contentType === 'text/markdown'){
                    vm.post.content += "<br><img src='"+vm.post.image+"' height='200px'/>";
                }
                userService.newPost(vm.post);
            });
        } else {
            userService.newPost(vm.post);
        };
        vm.post=null;
    }

    // edit a post that current user owned
    function editPost(id){
        var deferred = $q.defer();
        if (vm.image) {
            Upload.upload({
                url: "https://api.cloudinary.com/v1_1/dbodiislg/upload",
                data: {
                    upload_preset: "b1gyt5ss",
                    file: vm.image
                },
                headers:{
                    "Authorization": undefined
                }
            }).success(function(data){
                deferred.resolve(data);
                vm.edit.image = deferred.promise.$$state.value.url;
                if (vm.edit.contentType === 'text/markdown'){
                    vm.edit.content += "<br><img src='"+vm.edit.image+"' height='200px'/>";
                }
                userService.editPost(id, vm.edit);
            });
        } else {
            userService.editPost(id, vm.edit);
        }
        vm.edit=null;
    }

    // delete the post that current user owned
    function deletePost(id){
        userService.deletePost(id);
    }

    // make comment for posts that current user can see
    function makeComment(id){
        userService.newComment(id, vm.comment);
        vm.comment=null
    }
    // delete a comment in a post which current user owned
    function deleteComment(id){
        userService.deleteComment(id);
    }

    function sendRemoteRequest(remotefriend){
        var request = {
            "author": {
                "id": remotefriend.id,
                "host": remotefriend.host,
                "displayName": remotefriend.displayName,
            },
            "friend": {
                "id": vm.currentAuthor.id,
                "host": vm.currentAuthor.host,
                "displayName": vm.currentAuthor.displayName,
                "url": vm.currentAuthor.url,
            }
        };
        userService.sendRemoteFriendRequest(request);
        alert("Remote Friend Request Send");
    }
}

// My Posts Controller
function myPostController(userService, $q, $route, $rootScope, $location,Upload, $interval) {
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.myPosts = [];
    vm.deletePost=deletePost;
    vm.edit = null;
    vm.editPost = editPost;
    vm.deleteComment=deleteComment;
    vm.comment=null;
    vm.makeComment = makeComment;
    vm.allAuthor = [];
    vm.searchArray = null;

    initController();

    function initController() {
        loadAllMyPost();
        loadAllAuthor();
    }

    // load all post current user made
    function loadAllMyPost(){
        userService.getPost(vm.currentAuthor.id)
            .then(function (allpost) {
                vm.myPosts = allpost.results;
                $location.path('/myposts');
            });
    }

    $interval(checkUpdate,1000);
    function checkUpdate(){
        userService.getPost(vm.currentAuthor.id)
            .then(function (allpost) {
                var newposts = allpost.results;
                var res = angular.equals(newposts,vm.myPosts);
                if (!res){
                    vm.myPosts = newposts;
                };
            });
    }

    // load all author
    function loadAllAuthor(){
        userService.getAllAuthor()
            .then(function (allAuthor) {
                vm.allAuthor = allAuthor.data.results;
            });
    }

    // delete the post that current user owned
    function deletePost(id){
        userService.deletePost(id);
    }

    // edit a post that current user owned
    function editPost(id){
        var deferred = $q.defer();
        if (vm.image) {
            Upload.upload({
                url: "https://api.cloudinary.com/v1_1/dbodiislg/upload",
                data: {
                    upload_preset: "b1gyt5ss",
                    file: vm.image
                },
                headers:{
                    "Authorization": undefined
                }
            }).success(function(data){
                deferred.resolve(data);
                vm.edit.image = deferred.promise.$$state.value.url;
                if (vm.edit.contentType === 'text/markdown'){
                    vm.edit.content += "<br><img src='"+vm.edit.image+"' height='200px'/>";
                }
                userService.editPost(id, vm.edit);
            });
        } else {
            userService.editPost(id, vm.edit);
        }
        vm.edit=null;
    }

    // make a comment for post with id
    function makeComment(id){
        userService.newComment(id, vm.comment);
        vm.comment=null;
    }

    // delete a comment in a post which current user owned
    function deleteComment(id){
        userService.deleteComment(id);
    }
}

// My Friend Controller
function myFriendController(userService, $rootScope) {
    var vm = this;

    vm.myFriends = [];
    vm.friend =null;
    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.allAuthor = [];
    vm.searchArray = null;

    initController();

    function initController() {
        loadAllMyFriend();
        loadAllAuthor();
    }

    // load all friends that current user have
    function loadAllMyFriend(){
        userService.getAllMyFriend(vm.currentAuthor.id)
            .then(function (myFriends) {
                vm.myFriends = myFriends.friends;
            });
    }

    // get all author
    function loadAllAuthor(){
        userService.getAllAuthor()
            .then(function (allAuthor) {
                vm.allAuthor = allAuthor.data.results;
            });
    }
}

// Friend Posts Controller
function friendPostController(userService,$route, $rootScope, $routeParams, $location, $interval) {
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.friend_id = $routeParams.id;
    vm.friendPosts=[];
    vm.friend = [];
    vm.allAuthor = [];
    vm.searchArray = null;
    vm.allFriend = null;
    vm.deleteFriend = deleteFriend;
    vm.friendRequest = friendRequest;
    vm.comment=null;
    vm.makeComment = makeComment;
    vm.deleteComment = deleteComment;

    initController();

    function initController() {
        getFriendPost();
        loadAllAuthor();
        getFriend();
        getAllAuthorFriend();
    }

    // load all authors
    function loadAllAuthor(){
        userService.getAllAuthor()
            .then(function (allAuthor) {
                vm.allAuthor = allAuthor.data.results;
            });
    }

    // get all posts that current user's friend have
    function getFriendPost(){
        if (vm.friend_id===vm.currentAuthor.id){
            $location.path('/myposts');
        } else {
            userService.getPost(vm.friend_id)
                .then(function (friendPosts) {
                    vm.friendPosts = friendPosts.results;
                });
        }
    }

    $interval(checkUpdate,1000);
    function checkUpdate(){
        userService.getPost(vm.friend_id)
            .then(function (friendPosts) {
                var newposts = friendPosts.results;
                var res = angular.equals(newposts,vm.friendPosts);
                if (!res){
                    vm.friendPosts = newposts;
                }
            });
    }

    // get the information of current user's friend
    function getFriend(){
        userService.getAuthorById(vm.friend_id)
            .then(function (friend) {
                vm.friend = friend;
            });
    }

    // get all friend
    function getAllAuthorFriend(){
        userService.getAllMyFriend(vm.currentAuthor.id)
            .then(function (myFriends) {
            vm.allFriend = myFriends.friends;
        });
    }

    // make comment for post with id
    function makeComment(id){
        userService.newComment(id, vm.comment);
        vm.comment=null;
    }

    // unfriend with an author
    function deleteFriend(id){
        userService.removeFriend(id);
        $route.reload();
    }

    // to be friend with an author
    function friendRequest(id){
        userService.sendFriendRequest(id);
        $route.reload();
    }

    // delete a comment in a post which current user owned
    function deleteComment(id){
        userService.deleteComment(id);
    }
}

function myInfoController(userService, $q, $route, $location, $rootScope, FlashService, Upload) {
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.updateAuthor = updateAuthor;
    vm.update=null;
    vm.allAuthor = [];
    vm.searchArray = null;

    initController();

    function initController() {
        loadAllAuthor();
    }

    // load all authors
    function loadAllAuthor(){
        userService.getAllAuthor()
            .then(function (allAuthor) {
                vm.allAuthor = allAuthor.data.results;
            });
    }

    // update author's informations
    function updateAuthor(){
        var deferred = $q.defer();
        if (vm.avatar) {
            Upload.upload({
                url: "https://api.cloudinary.com/v1_1/dbodiislg/upload",
                data: {
                    upload_preset: "b1gyt5ss",
                    file: vm.avatar
                },
                headers:{
                    "Authorization": undefined
                }
            }).success(function(data){
                deferred.resolve(data);
                vm.update.avatar = deferred.promise.$$state.value.url;
                userService.updateAuthor(vm.currentAuthor.id, vm.update);
                alert("You will be logged out, log in again to complete update");
                $location.path('/login');
            })
        } else {
            userService.updateAuthor(vm.currentAuthor.id, vm.update);
            alert("You will be logged out, log in again to complete update");
            $location.path('/login');
        }
    }
}

function githubController(userService, $q, $route, $location, $rootScope, FlashService, Upload, $interval){
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.github = null;
    vm.makePost = makePost;
    vm.post = null;
    vm.allAuthor = [];
    vm.searchArray = null;

    initController();

    function initController() {
        loadGitHub();
        loadAllAuthor();
    }

    // load all authors
    function loadAllAuthor(){
        userService.getAllAuthor()
            .then(function (allAuthor) {
                vm.allAuthor = allAuthor.data.results;
            });
    }

    // load all github activities for following author and youself
    function loadGitHub(){
        userService.getGithub(vm.currentAuthor.github)
            .then(function (mygit) {
                vm.github=mygit.data;
            });
    }

    $interval(checkUpdate,1000);
    function checkUpdate(){
        userService.getGithub(vm.currentAuthor.github)
            .then(function (mygit) {
                var newgit = mygit.data;
                var res = angular.equals(newgit,vm.github);
                if (!res){
                    vm.github = newgit;
                }
            });
    }

    // make a new post
    function makePost(){
        vm.dataLoading = true;
        var deferred = $q.defer();
        if (vm.image) {
            Upload.upload({
                url: "https://api.cloudinary.com/v1_1/dbodiislg/upload",
                data: {
                    upload_preset: "b1gyt5ss",
                    file: vm.image
                },
                headers:{
                    "Authorization": undefined
                }
            }).success(function(data){
                deferred.resolve(data);
                vm.post.image = deferred.promise.$$state.value.url;
                if (vm.post.contentType === 'text/markdown'){
                    vm.post.content += "<br><img src='"+vm.post.image+"' height='200px'/>";
                }
                userService.newPost(vm.post);
            });
        } else {
            userService.newPost(vm.post);
        };
        vm.post = null;
    }


}

function friendRequestController(userService, $route, $rootScope, $interval) {
    var vm = this;

    vm.currentAuthor = $rootScope.globals.currentUser.author;
    vm.allAuthor = [];
    vm.searchArray = null;
    vm.sendRequest= null;
    vm.accept = accept;
    vm.reject = reject;
    vm.acceptRemote = acceptRemote;

    initController();

    function initController() {
        loadAllAuthor();
        loadAllRequest();
    }

    // load all authors
    function loadAllAuthor(){
        userService.getAllAuthor()
            .then(function (allAuthor) {
                vm.allAuthor = allAuthor.data.results;
            });
    }

    // load all request
    function loadAllRequest(){
        userService.request()
            .then(function(response){
                vm.sendRequest = response.data.results;
            })
    }

    $interval(checkUpdate,1000);
    function checkUpdate(){
        userService.request()
            .then(function(response){
                var newreq = response.data.results;
                var res = angular.equals(newreq, vm.sendRequest);
                if (!res){
                    vm.sendRequest = newreq;
                }
            })
    }

    // accept the friend request
    function accept(id){
        userService.acceptRequest(id);
        $route.reload();
    }

    // reject friend request
    function reject(id){
        userService.rejectRequest(id);
        $route.reload();
    }

    // accept remote friend request
    function acceptRemote(remotefriend){
        var request = {
            "author": {
                "id": remotefriend.id,
                "host": remotefriend.host,
                "displayName": remotefriend.displayName,
            },
            "friend": {
                "id": vm.currentAuthor.id,
                "host": vm.currentAuthor.host,
                "displayName": vm.currentAuthor.displayName,
                "url": vm.currentAuthor.url,
            }
        };
        userService.sendRemoteFriendRequest(request);
        alert("Remote Friend Request Accpeted");
        $route.reload();
    }
}

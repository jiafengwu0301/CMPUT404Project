// Reference: http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

// the userService is used for making POST, PUT, GET, DELETE request to server, either send a JSON to server or receive a JSON from server and return JSON back to controller

﻿angular
    .module('myApp')
    .factory('userService', userService);

userService.$inject = ['$http','$rootScope','$location','$cookies'];
function userService($http,$rootScope,$location,$cookies) {
    var service = {};

    service.getAllPost = getAllPost;
    service.newPost = newPost;
    service.getPost = getPost;
    service.deletePost = deletePost;
    service.editPost = editPost;
    service.getAllMyFriend=getAllMyFriend;
    service.getFriendPosts =getFriendPosts;
    service.createUser=createUser;
    service.getAuthorById=getAuthorById;
    service.newComment = newComment;
    service.deleteComment = deleteComment;
    service.updateAuthor = updateAuthor;
    service.getAllAuthor = getAllAuthor;
    service.removeFriend = removeFriend;
    service.sendFriendRequest = sendFriendRequest;
    service.getGithub = getGithub;
    service.request = request;
    service.acceptRequest = acceptRequest;
    service.rejectRequest = rejectRequest;

    return service;

    var host_heroku = "socialnets404.herokuapp.com";
    var host_heroku_local = "127.0.0.1:8000";

    // create a user
    function createUser(author){
        return $http.post('https://'+host_heroku+'/socialnet/authors/create/',author).then(handleSuccess, handleError('Error'));
    }

    // update author's informations
    function updateAuthor(id, update){
        return $http.put('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/'+id+'/update/', update)
    }

    // get all posts that current use has permission
    function getAllPost(){
        return $http.get('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/posts/').then(handleSuccess, handleError('Error'));
    }

    // get all author
    function getAllAuthor(){
        return $http.get('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/')
    }

    // get Github avtivity
    function getGithub(username){
        return $http({method:"GET",url:"https://api.github.com/users/"+username+"/events", headers:{"Authorization":undefined}})
    }

    // get post by id
    function getPost(id){
        return $http.get('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/'+id+'/posts/').then(handleSuccess, handleError('Error'));
    }

    // make a new post for current user
    function newPost(post){
        var a = JSON.stringify(post);
        return $http.post('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/posts/create/',JSON.parse(a)).then(handleSuccess, handleError('Error'));
    }

    // delete a post by id
    function deletePost(id){
        return $http.delete('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/posts/'+id+'/destroy/');
    }

    // edit a post by id and the post with edit
    function editPost(id, post){
        var a = JSON.stringify(post);
        return $http.put('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/posts/'+id+'/update/', JSON.parse(a));
    }

    // get all friends by author id
    function getAllMyFriend(id){
        return $http.get('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/'+id+'/network/').then(handleSuccess, handleError('Error'));
    }

    // get friend's post by friend's id
    function getFriendPosts(id){
        return $http.get('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/'+id+'/posts/').then(handleSuccess, handleError('Error'));
    }

    // get an author by its id
    function getAuthorById(id){
        return $http.get('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/'+id+'/').then(handleSuccess, handleError('Error'));
    }

    // get current author's information
    function getAuthorForAuthentication(id,username,password){
        return $http.get('https://'+username+':'+password+'@'+host_heroku+'/socialnet/authors/'+id+'/').then(handleSuccess, handleError('Error'));
    }

    // make a new comment by post id and comment data
    function newComment(id,comment){
        return $http.post('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/posts/'+id+'/comments/create/',comment).then(handleSuccess, handleError('Error'));
    }

    // delete a comment by its id
    function deleteComment(id){
        return $http.delete('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/comments/'+id+'/destroy/').then(handleSuccess, handleError('Error'));
    }

    // unfriend with an author
    function removeFriend(id){
        return $http.delete('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/friends/unfriend/'+id+'/')
    }

    // send a friend request to an author
    function sendFriendRequest(id){
        return $http.post('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/friend_request/'+id+'/')
    }

    // get all request you send and receive
    function request(){
        return $http.get('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/friends/friend_requests/')
    }

    // accept a friend request
    function acceptRequest(id){
        return $http.post('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/friend_request/accept/'+id+'/')
    }

    // reject a friend request
    function rejectRequest(id){
        return $http.delete('https://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@'+host_heroku+'/socialnet/authors/friend_request/reject/'+id+'/')
    }

    // if success, return the data
    function handleSuccess(res) {
        return res.data;
    }

    // if not success, return an error message
    function handleError(error) {
        return function () {
            return { success: false, message: error };
        };
    }
}

// http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

﻿angular
    .module('myApp')
    .factory('UserService', UserService);

UserService.$inject = ['$http','$rootScope','$location','$cookies'];
function UserService($http,$rootScope,$location,$cookies) {
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
    //service.logIn = logIn;

    return service;

    function createUser(author){
        return $http.post('http://127.0.0.1:8000/socialnet/authors/create/',author).then(handleSuccess, handleError('Error'));
    }

/*    function logIn(info){

        var req ={
            method : "POST",
            url: "http://127.0.0.1:8000/socialnet/auth/",
            headers : {
                'Content-Type' : 'application/json',
            },
            data : info
        };
        // alert(info.username);
        // $location.path('/')
        // alert($cookies['csrftoken']);
        return $http(req).then(handleSuccess, handleError('Error'));

    }*/

    function getAllPost(){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/posts/').then(handleSuccess, handleError('Error'));
    }
    // change name to getPosts
    function getPost(id){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/authors/'+id+'/posts/').then(handleSuccess, handleError('Error'));
    }

    function newPost(post){
        var a = JSON.stringify(post);
        return $http.post('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/posts/create/',JSON.parse(a)).then(handleSuccess, handleError('Error'));
    }

    function deletePost(id){
        return $http.delete('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/posts/'+id+'/destroy/');
    }

    function editPost(id, post){
        var a = JSON.stringify(post);
        return $http.put('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/posts/'+id+'/update/', JSON.parse(a));
    }

    function getAllMyFriend(id){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/authors/'+id+'/friends/').then(handleSuccess, handleError('Error'));
    }

    function getFriendPosts(id){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/authors/'+id+'/posts/').then(handleSuccess, handleError('Error'));
    }

    function getAuthorById(id){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/authors/'+id+'/').then(handleSuccess, handleError('Error'));
    }

    function getAuthorForAuthentication(id,username,password){
        return $http.get('http://'+username+':'+password+'@127.0.0.1:8000/socialnet/authors/'+id+'/').then(handleSuccess, handleError('Error'));
    }

    // private functions

    function handleSuccess(res) {
        //alert(res.data.github)
        return res.data;
    }

    function handleError(error) {
        return function () {
            return { success: false, message: error };
        };
    }
}

// http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

﻿angular
    .module('myApp')
    .factory('UserService', UserService);

UserService.$inject = ['$http','$rootScope'];
function UserService($http,$rootScope) {
    var service = {};

    service.GetAllPost = GetAllPost;
    service.NewPost = NewPost;
    service.GetAllMyPost = GetAllMyPost;
    service.DeletePost = DeletePost;
    service.EditPost = EditPost;
    service.GetAllMyFriend=GetAllMyFriend;
    service.GetFriendPosts =GetFriendPosts;
    service.CreateUser=CreateUser;
    service.getAuthorById=getAuthorById;

    return service;

    function CreateUser(author){
        return $http.post('http://127.0.0.1:8000/socialnet/authors/create/',author).then(handleSuccess, handleError('Error'));
    }

    function GetAllPost(){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/posts/').then(handleSuccess, handleError('Error'));
    }
    // change name to getPosts
    function GetAllMyPost(id){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/authors/'+id+'/posts/').then(handleSuccess, handleError('Error'));
    }

    function NewPost(post){
        var a = JSON.stringify(post);
        return $http.post('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/posts/create/',JSON.parse(a)).then(handleSuccess, handleError('Error'));
    }

    function DeletePost(id){
        return $http.delete('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/posts/'+id+'/destroy/');
    }

    function EditPost(id, post){
        var a = JSON.stringify(post);
        return $http.put('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/posts/'+id+'/update/', JSON.parse(a));
    }

    function GetAllMyFriend(id){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/authors/'+id+'/friends/').then(handleSuccess, handleError('Error'));
    }

    function GetFriendPosts(id){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/authors/'+id+'/posts/').then(handleSuccess, handleError('Error'));
    }

    function getAuthorById(id){
        return $http.get('http://'+Base64.decode($rootScope.globals.currentUser.authdata)+'@127.0.0.1:8000/socialnet/authors/'+id+'/').then(handleSuccess, handleError('Error'));
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

// http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example
// use for local test
angular
    .module('myApp')
    .factory('UserService', UserService);

UserService.$inject = ['$timeout', '$filter', '$q'];
function UserService($timeout, $filter, $q) {

    var service = {};

    service.GetAllUser = GetAllUser;
    service.GetByUserId = GetByUserId;
    service.GetByUsername = GetByUsername;
    service.CreateUser = CreateUser;
    service.UpdateUser = UpdateUser;
    service.DeleteUser = DeleteUser;
    service.GetAllPost = GetAllPost;
    service.NewPost = NewPost;

    return service;

    function GetAllUser() {
        return JSON.parse(localStorage.users)
    }

    function GetAllPost(){
        return JSON.parse(localStorage.posts)
    }

    function GetByUserId(id) {
        var deferred = $q.defer();
        var filtered = $filter('filter')(getUsers(), { id: id });
        var user = filtered.length ? filtered[0] : null;
        deferred.resolve(user);
        return deferred.promise;
    }

    function GetByUsername(username) {
        var deferred = $q.defer();
        var filtered = $filter('filter')(getUsers(), { username: username });
        var user = filtered.length ? filtered[0] : null;
        deferred.resolve(user);
        return deferred.promise;
    }

    function CreateUser(user) {
        var deferred = $q.defer();

        // simulate api call with $timeout
        $timeout(function () {
            GetByUsername(user.username)
                .then(function (duplicateUser) {
                    if (duplicateUser !== null) {
                        deferred.resolve({ success: false, message: 'Username "' + user.username + '" is already taken' });
                    } else {
                        var users = getUsers();

                        // assign id
                        var lastUser = users[users.length - 1] || { id: 0 };
                        user.id = lastUser.id + 1;

                        // save to local storage
                        users.push(user);
                        setUsers(users);

                        deferred.resolve({ success: true });
                    }
                });
        }, 1000);

        return deferred.promise;
    }

    function UpdateUser(user) {
        var deferred = $q.defer();

        var users = getUsers();
        for (var i = 0; i < users.length; i++) {
            if (users[i].id === user.id) {
                users[i] = user;
                break;
            }
        }
        setUsers(users);
        deferred.resolve();

        return deferred.promise;
    }

    function DeleteUser(id) {
        var deferred = $q.defer();

        var users = getUsers();
        for (var i = 0; i < users.length; i++) {
            var user = users[i];
            if (user.id === id) {
                users.splice(i, 1);
                break;
            }
        }
        setUsers(users);
        deferred.resolve();

        return deferred.promise;
    }

    function NewPost(post){
        var posts = JSON.parse(localStorage.posts)
        var lastPost = posts[posts.length - 1] || { id: 0 };
        post.id = lastPost.id + 1;
        posts.push(post);
        localStorage.posts = JSON.stringify(posts);
    }

    // private functions

    function getUsers() {
        if(!localStorage.users){
            localStorage.users = JSON.stringify([]);
        }

        return JSON.parse(localStorage.users);
    }

    function getPosts() {
        if(!localStorage.posts){
            localStorage.posts = JSON.stringify([]);
        }

        return JSON.parse(localStorage.posts);
    }

    function setUsers(users) {
        localStorage.users = JSON.stringify(users);
    }
}

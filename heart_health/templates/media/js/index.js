function beginNoLogin() {
    if(isUserLoggedIn){
        window.location.href = '/assess/basic/';
    } else {
        window.location.href = '/register/';
    }
}

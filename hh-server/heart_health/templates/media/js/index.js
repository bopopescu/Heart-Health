function beginNoLogin() {
    if(isUserLoggedIn){
        window.location.href = '/basic/';
    } else {
        window.location.href = '/register/';
    }
}

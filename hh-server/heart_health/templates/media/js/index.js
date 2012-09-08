function beginNoLogin() {
    if(isUserLoggedIn){
        window.location.href = '/begin/';
    } else {
        window.location.href = '/register/';
    }
}

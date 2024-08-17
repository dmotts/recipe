function printRecipe() {
    window.print();
}

function bookmarkPage() {
    const title = document.title;
    const url = window.location.href;

    if (window.sidebar && window.sidebar.addPanel) { // Firefox <23
        window.sidebar.addPanel(title, url, '');
    } else if (window.external && ('AddFavorite' in window.external)) { // IE Favorites
        window.external.AddFavorite(url, title);
    } else if (window.opera && window.print || window.sidebar && !(window.sidebar instanceof Node)) { // Opera <15 and Safari
        this.title = title;
        return true;
    } else { // For browsers that do not support the bookmark feature
        alert('Press ' + (navigator.userAgent.toLowerCase().indexOf('mac') != -1 ? 'Cmd' : 'Ctrl') + ' + D to bookmark this page.');
    }
}

function sharePage() {
    if (navigator.share) {
        navigator.share({
            title: document.title,
            text: 'Check out this recipe!',
            url: window.location.href
        }).then(() => {
            console.log('Thanks for sharing!');
        }).catch(console.error);
    } else {
        alert('Your browser does not support the native sharing feature. Please copy the URL manually.');
    }
}

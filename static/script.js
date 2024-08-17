function printRecipe() {
    window.print();
}

function bookmarkPage() {
    alert('Press ' + (navigator.userAgent.toLowerCase().indexOf('mac') != -1 ? 'Cmd' : 'Ctrl') + ' + D to bookmark this page.');
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

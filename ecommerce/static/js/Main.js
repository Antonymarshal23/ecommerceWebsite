
var updateBtns = document.getElementsByClassName('update-cart')

var wishBtns = document.getElementsByClassName('update-wishlist')


document.addEventListener('DOMContentLoaded', () => {
    for(i = 0; i < updateBtns.length; i++){
        updateBtns[i].addEventListener('click', function(){
            var productId = this.dataset.product
            var action = this.dataset.action
            
            if (user == 'AnonymousUser'){
                addCookieItem(productId, action)
            }
            else{
                updateUserOrder(productId, action)
            }
        })
    }

});

document.addEventListener('DOMContentLoaded', () => {
    for(i = 0; i < wishBtns.length; i++){
        wishBtns[i].addEventListener('click', function(){
            var productId = this.dataset.product
            var action = this.dataset.action
           
            if (user == 'AnonymousUser'){
                addCookieItemWishlist(productId, action)
            }
            else{
                updateUserWishlist(productId, action)
                
            }
        })
    }
});

// for cart page 
function addCookieItem(productId, action){
    console.log(" user not looged in")

    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -= 1
        
        if (cart[productId]['quantity'] <= 0){
            console.log("Item should be deleted")
            delete cart[productId]
        }
    }
    console.log("cart", cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/" 
    location.reload()
}
    
// for wishlist
function addCookieItemWishlist(productId, action){
    if (action == 'add'){
        if (wishlist[productId] == undefined){
            wishlist[productId] = {'quantity': 1}
        }
    }
    
    if (action == 'remove'){
        delete wishlist[productId]
    }
    
    document.cookie = 'wishlist=' + JSON.stringify(wishlist) + ";domain=;path=/" 
    location.reload()
}

// for cart post methods
function updateUserOrder(productId, action){
    console.log("data sending")

    url = "/update_item/"

    fetch(url, {
        method: 'POST',
        headers: {
            'ContentType': 'application/json',
            'X-CSRFToken': csrftoken,

        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log("data:", data)
        location.reload()
    })
}

// for wishlist post method 
function updateUserWishlist(productId, action){
    console.log("data sending")

    url = "/update_wishlist/"
    
    fetch(url, {
        method: 'POST',
        headers: {
            'ContentType': 'application/json',
            'X-CSRFToken': csrftoken,

        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log("data:", data)
        location.reload()
    })
}
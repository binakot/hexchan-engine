var RefPopup = function(props) {
    var POPUP_VERTICAL_OFFSET = 5;

    var popupIsVisible = false;


    function init() {
        document.addEventListener('mouseover', onMouseOver);
        document.addEventListener('mouseout', onMouseOut);
    }


    function destroy() {
        document.removeEventListener('mouseover', onMouseOver);
        document.removeEventListener('mouseout', onMouseOut);
    }


    function onMouseOver(ev) {
        if (ev.target.classList.contains('js-ref')) {
            var hid = ev.target.innerHTML.replace('&gt;&gt;', '');
            var url = ev.target.getAttribute('href').replace('#', '');
            var postEl = document.querySelector('.js-post[data-hid="' + hid + '"]');

            popupIsVisible = true;

            if (postEl) {
                showPopup(ev.target, hid, postEl.cloneNode(true));
            } else {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', url, true);
                xhr.onreadystatechange = function () { // (3)
                    if (xhr.readyState !== 4) return;

                    if (xhr.status !== 200) {
                        console.error('Error occured when requesting post', xhr.status, xhr.statusText);
                    } else {
                        showPopup(ev.target, hid, xhr.responseText);
                    }
                };
                xhr.send();
            }
        }
    }


    function onMouseOut(ev) {
        popupIsVisible = false;
        hidePopups();
    }


    function showPopup(target, hid, content) {
        if (popupIsVisible) {
            var targetBox = target.getBoundingClientRect();

            var popupEl = document.createElement('div');

            if (typeof content === 'string') {
                popupEl.innerHTML = content;
            } else if (content instanceof Element) {
                popupEl.appendChild(content);
            }

            popupEl.className = 'ref-popup js-ref-popup';
            popupEl.setAttribute('data-hid', hid);
            popupEl.style.top = targetBox.top + targetBox.height + POPUP_VERTICAL_OFFSET + window.pageYOffset + 'px';
            popupEl.style.left = 0 + 'px';

            var elementsToRemoveInPopup = popupEl.querySelectorAll('.js-toggle-thread, .js-toggle-post');
            var elementToRemove;
            for (var i = 0; i < elementsToRemoveInPopup.length; i++) {
                elementToRemove = elementsToRemoveInPopup[i];
                elementToRemove.remove();
            }

            var popupContainer = document.querySelector('.js-popup-container');
            popupContainer && popupContainer.appendChild(popupEl);
        }
    }


    function hidePopups() {
        var popupEls = document.querySelectorAll('.js-ref-popup');
        for (var i =0; i < popupEls.length; i += 1) {
            popupEls[i].remove();
        }
    }


    init();
    return {
        destroy: destroy,
    };
};


export default RefPopup;

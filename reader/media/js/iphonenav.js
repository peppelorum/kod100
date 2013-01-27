(function() {

var animateX = -20;
var animateInterval = 24;

var currentPage = null;
var currentDialog = null;
var currentWidth = 0;
var currentHash = location.hash;
var hashPrefix = "#_";
var pageHistory = [];
    
$(function() {
    showPage($('ul[selected=true]')[0]);
    setInterval(checkOrientAndLocation, 300);
    setTimeout(scrollTo, 0, 0, 1);

    $('#mark_read').click(function mark_read() {
        var id = $('#contents').data('post');
        setTimeout(function() { $.post('/reader/action/', {id: id, ajax: 1, read: 1}); }, 1);
        var post_link = $('#post_link' + id);
        var li = post_link.parent();
        var ul = li.parent();
        li.remove();
        if (ul.children().length == 0)
        {
            ul.remove();
            var feed_id = ul.attr('id');
            feed_id = feed_id.replace(/feed/, 'feed_link');
            li = $('#' + feed_id).parent();
            ul = li.parent();
            li.remove();
            if (ul.children().length == 0)
            {
                ul.remove();
                var cat_id = ul.attr('id');
                cat_id = cat_id.replace(/cat/, 'cat_link');
                li = $('#'+cat_id).remove();
                window.history.go(-3);
            }
            else
                window.history.go(-2);
        }
        else
            window.history.go(-1);
    });

    $('a').click(function(event) {
        if (this.hash && this.hash.length > 1)
        {
            event.preventDefault();
            if(this.id == 'homeButton') {
                $('.panel_button').hide();
                pageHistory.pop();
                showPage($('#'+pageHistory.pop())[0], true);
            }
            else {
                var page = document.getElementById(this.hash.substr(1));
                showPage(page);
            }
        }
    });

    $('.post_link').click(function () {
        var id = $(this).attr('id').replace(/post_link/, '');
        var title = $(this).attr('title');
        $('#contents').hide();
        $('#loading').show();
        $('#contents').load('/reader/post/' + id + '/', function() {
            $('#contents').data('post', id);
            $('#loading').hide();
            $('#contents').show();
            $('#mark_read').show();
        });
    });
});

function checkOrientAndLocation()
{
    if (window.outerWidth != currentWidth)
    {
        currentWidth = window.outerWidth;

        var orient = currentWidth == 320 ? "profile" : "landscape";
        document.body.setAttribute("orient", orient);
    }

    if (location.hash != currentHash)
    {
        currentHash = location.hash;

        var pageId = currentHash.substr(hashPrefix.length);
        var page = document.getElementById(pageId);
        if (page)
        {
            var index = pageHistory.indexOf(pageId);
            var backwards = index != -1;
            if (backwards)
                pageHistory.splice(index, pageHistory.length);
                
            showPage(page, backwards);
        }
    }
}
    
function showPage(page, backwards)
{
    if (currentDialog)
    {
        currentDialog.removeAttribute("selected");
        currentDialog = null;
    }

    if (page.className.indexOf("dialog") != -1)
    {
        showDialog(page);
    }
    else
    {        
        location.href = currentHash = hashPrefix + page.id;
        pageHistory.push(page.id);

        var fromPage = currentPage;
        currentPage = page;

        var pageTitle = document.getElementById("pageTitle");
        pageTitle.innerHTML = page.title || "";

        var homeButton = document.getElementById("homeButton");
        if (homeButton)
            homeButton.style.display = ("#"+page.id) == homeButton.hash ? "none" : "inline";

        if (fromPage)
            setTimeout(swipePage, 0, fromPage, page, backwards);
    }
}

function swipePage(fromPage, toPage, backwards)
{        
    toPage.style.left = "100%";
    toPage.setAttribute("selected", "true");
    scrollTo(0, 1);
    
    var percent = 100;
    var timer = setInterval(function()
    {
        percent += animateX;
        if (percent <= 0)
        {
            percent = 0;
            fromPage.removeAttribute("selected");
            clearInterval(timer);
        }

        fromPage.style.left = (backwards ? (100-percent) : (percent-100)) + "%"; 
        toPage.style.left = (backwards ? -percent : percent) + "%"; 
    }, animateInterval);
}

function showDialog(form)
{
    currentDialog = form;
    form.setAttribute("selected", "true");
    
    form.onsubmit = function(event)
    {
        event.preventDefault();
        form.removeAttribute("selected");

        var index = form.action.lastIndexOf("#");
        if (index != -1)
            showPage(document.getElementById(form.action.substr(index+1)));
    }

    form.onclick = function(event)
    {
        if (event.target == form)
            form.removeAttribute("selected");
    }
}

})();


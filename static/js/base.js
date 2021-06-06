$(document).ready(function() {
    // SideNav Button Initialization
    $(".button-collapse").sideNav2();
    // SideNav Scrollbar Initialization
    var sideNavScrollbar = document.querySelector('.custom-scrollbar');
    var ps = new PerfectScrollbar(sideNavScrollbar);
    //Activate Toast Messages
    $('.toast').toast('show');
    //Detect client time zone
    const timeZoneName = Intl.DateTimeFormat().resolvedOptions().timeZone;
    document.cookie = 'timezone=' + encodeURIComponent(timeZoneName) + '; path=/';
    // Sticky sidebar from MD Bootstrap
    $(function () {
        $(".sticky").sticky({
            topSpacing: 128,
            stopper: "#footer"
        });
    });
});
$(window).on('scroll', function() {
    releaseFixedSidebar();
});

/* Based upon "Make a Sidebar Always Visible Regardless of Scroll",
by Łukasz Nojek, 4-20-20, https://lukasznojek.com/blog/2020/04/make-a-sidebar-always-visible-regardless-of-scroll/ */
function releaseFixedSidebar() {
    const footer = $("footer");
    const topOfFooter = footer.offset().top;
    console.log("----top of footer:", topOfFooter);
    const sideMenuColumn = $(".side-menu-col");
    const sideMenu = $(".side-menu")
    const sideMenuTop = sideMenu.position().top;
    console.log("----sideMenu top:", sideMenuTop);
    const sideMenuHeight = sideMenu.outerHeight(false);
    const sideMenuBottom = sideMenuTop + sideMenuHeight;
    console.log("----sideMenu bottom:", sideMenuBottom);
    headerHeight = $("header").outerHeight(false);
    scrollPosition = window.scrollY;
    sideMenuCalc = scrollPosition + (headerHeight + sideMenuHeight);
    console.log("---sideMenuCalc:", sideMenuCalc);
    console.log("scrollTop:", scrollPosition);
    const myWindow = $(window).height();
    console.log("window height:", window);
    if(sideMenuCalc < topOfFooter) {
        $(sideMenuColumn).css({"position": "fixed"});
        $(".head-row").css({"transform": "translateX(30vw)"});
        console.log("side fixed");
    } else if((myWindow < sideMenuHeight) || (sideMenuCalc >= topOfFooter)) {
        $(sideMenuColumn).css({"position": "relative"});
        $(".head-row").css({"transform": "translateX(7vw)"});
        console.log("side relative - scrolls");
    }
}

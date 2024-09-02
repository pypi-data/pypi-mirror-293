$(document).ready(function() {
    const mainContent = $('.content');
    const toc = $('.right-sidebar ul');
    const tocItems = toc.find('a');
    const sections = mainContent.find('section');
    const offset = 100; // Adjust this value to change when the highlight switches

    $(window).on('scroll', function() {
        const scrollPosition = $(window).scrollTop();

        // Find the current section
        let currentSection = null;
        sections.each(function() {
            if ($(this).offset().top <= scrollPosition + offset) {
                currentSection = $(this);
            } else {
                return false; // Exit the loop early
            }
        });

        // Highlight the corresponding TOC item
        if (currentSection) {
            const currentId = currentSection.attr('id');
            tocItems.removeClass('active');

            tocItem = tocItems.filter(`[href="#${currentId}"]`).first();
            if (tocItem) {
                tocItem.addClass('active');
            } else {
                // If no ID found, we're likely at the top of the page
                // Highlight the first TOC item (assumed to be the root with href="#")
                tocItems.filter('[href="#"]').first().addClass('active');
            }
        } else {
            // If no current section found, we're likely at the very top of the page
            // Highlight the first TOC item
            tocItems.removeClass('active');
            tocItems.filter('[href="#"]').first().addClass('active');
        }
    });

    $(window).trigger('scroll');
});
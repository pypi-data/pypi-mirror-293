$(document).ready(function() {
    $('.cell_output.docutils.container.hide-output').each(function() {
        $(this).children('div').hide();
    });

    $('.cell_output.docutils.container.rotate-output').each(function() {
        var $rotateDiv = $(this);
        var $contentDivs = $rotateDiv.children('div');
        var currentIndex = 0;
        var rotationInterval;

        // Hide all content divs except the first one
        $contentDivs.hide().first().show();
        $contentDivs.first().css('opacity', '1');

        // Function to show next content div
        function showNextContent() {
            var currentScrollPosition = $contentDivs.eq(currentIndex).scrollLeft();
            // Hide current div
            $contentDivs.eq(currentIndex).hide();
            // Move to next div
            currentIndex = (currentIndex + 1) % $contentDivs.length;
            // Show next div
            var $nextDiv = $contentDivs.eq(currentIndex);
            $nextDiv.show();
            // Set the same scroll position for the new div
            $nextDiv.scrollLeft(currentScrollPosition);
        }

        // Function to start rotation
        function startRotation() {
            if (!rotationInterval) {
                rotationInterval = setInterval(showNextContent, 2000);
            }
        }

        // Function to stop rotation
        function stopRotation() {
            if (rotationInterval) {
                clearInterval(rotationInterval);
                rotationInterval = null;
            }
        }

        // Create an Intersection Observer
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    startRotation();
                } else {
                    stopRotation();
                }
            });
        }, {
            root: null, // viewport
            threshold: 0.1 // trigger when at least 10% of the target is visible
        });

        // Start observing the rotate div
        observer.observe($rotateDiv[0]);

        // Create SVG icons for pause and play
        var pauseIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/></svg>';
        var playIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';

        // Create and style the control button
        var $controlButton = $('<button>', {
            class: 'rotate-control-button',
            html: pauseIcon,
            css: {
                marginTop: '4px',
                background: 'rgba(0, 0, 0, 0)',
                border: 'none',
                borderRadius: '50%',
                width: '30px',
                height: '30px',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                cursor: 'pointer',
                color: 'white',
                padding: '0'
            }
        }).appendTo($rotateDiv);

        // Set relative positioning on rotate div to properly position the button
        $rotateDiv.css('position', 'relative');

        var isPaused = false;

        $controlButton.on('click', function() {
            if (isPaused) {
                startRotation();
                $(this).html(pauseIcon);
            } else {
                stopRotation();
                $(this).html(playIcon);
            }
            isPaused = !isPaused;
        });
    });

    $('.cell_output.collapse-output').each(function() {
        var $output = $(this);
        
        // Add the chevron
        $output.append('<div class="chevron"><svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>');
        
        // Initially collapse the output
        $output.addClass('collapsed');
        
        // Toggle collapse on chevron click
        $output.find('.chevron').on('click', function() {
            $output.toggleClass('collapsed');
        });
    });

    $('.cell_output.docutils.container.combine-output').each(function() {
        var $container = $(this);
        var combinedContent = '';
        
        // Find all pre elements and combine their content
        $container.find('pre').each(function() {
            combinedContent += $(this).html() + '\n';
        });
        
        // Create a new div with the combined content
        var $newDiv = $('<div class="output stream highlight-myst-ansi notranslate"><div class="highlight"><pre>' + combinedContent.trim() + '</pre></div></div>');
        
        // Remove all existing output divs
        $container.find('.output.stream').remove();
        
        // Remove all existing output stderr divs
        $container.find('.output.stderr').remove();

        // Append the new combined div after the output label
        $container.find('.output-label').after($newDiv);
    });
})
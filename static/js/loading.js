document.addEventListener('DOMContentLoaded', function() {
    // Get the loading container element
    const loadingContainer = document.getElementById('loading-container');
  
    // Add event listener to the links or buttons that trigger page transition
    const links = document.querySelectorAll('a'); // Select all anchor tags, you can modify the selector as needed
  
    links.forEach(function(link) {
      link.addEventListener('click', function(event) {
        // Check if the clicked link is the "About" link
        if (link.getAttribute('href') === '#about') {
          // Do not show the loading spinner for the "About" link
          return;
        }
  
        // Show the loading spinner
        loadingContainer.style.display = 'block';
  
        // Optional: Delay page transition to show loading spinner for a certain duration
        setTimeout(function() {
          // Allow the link to proceed with the default behavior (navigate to the next page)
          // or use your preferred method to load the next page content
        }, 1000); // Change the delay duration as needed
      });
    });
  });
  
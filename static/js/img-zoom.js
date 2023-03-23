const itemImages = document.querySelectorAll('#item-image');

// Add a click event listener to each image
itemImages.forEach(itemImage => {
  itemImage.addEventListener('click', () => {
    // Create a new image element to display the zoomed view
    const zoomedImage = document.createElement('img');

    // Set the source of the zoomed image to the same as the original image
    zoomedImage.src = itemImage.src;

    // Set some styling properties for the zoomed image
    zoomedImage.style.position = 'fixed';
    zoomedImage.style.top = '0';
    zoomedImage.style.left = '0';
    zoomedImage.style.width = '100%';
    zoomedImage.style.height = '100%';
    zoomedImage.style.objectFit = 'contain';
    zoomedImage.style.zIndex = '9999';
    zoomedImage.style.cursor = 'zoom-out';

    // Add a click event listener to the zoomed image to remove it from the DOM
    zoomedImage.addEventListener('click', () => {
      zoomedImage.remove();
    });

    // Add the zoomed image to the DOM
    document.body.appendChild(zoomedImage);
  });
});
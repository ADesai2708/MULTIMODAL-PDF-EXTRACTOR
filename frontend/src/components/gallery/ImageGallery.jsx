function ImageGallery({ images }) {

  if (!images.length) return null;

  return (

    <div className="mt-6">

      <h2 className="font-semibold mb-4">
        Referenced Images
      </h2>

      <div className="grid grid-cols-3 gap-4">

        {images.map((img, index) => (

          <div
            key={index}
            className="
              bg-white
              border
              rounded-xl
              overflow-hidden
            "
          >

            <img
              src={img.url}
              alt={img.name}
              className="
                h-40
                w-full
                object-cover
              "
            />

            <div className="p-3 text-sm">
              {img.name}
            </div>

          </div>

        ))}

      </div>

    </div>

  );
}

export default ImageGallery;
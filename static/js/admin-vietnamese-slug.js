(function () {
    function vietnameseSlug(value) {
        return (value || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[\u0111\u00f0]/g, 'd')
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '')
            .replace(/-{2,}/g, '-');
    }

    function bindSlug(sourceId, slugId) {
        var source = document.getElementById(sourceId);
        var slug = document.getElementById(slugId);
        if (!source || !slug) {
            return;
        }

        var userEditedSlug = Boolean(slug.value && slug.value !== vietnameseSlug(source.value));
        var previousGenerated = vietnameseSlug(source.value);

        slug.addEventListener('input', function () {
            userEditedSlug = document.activeElement === slug;
        });

        function updateSlug() {
            if (userEditedSlug) {
                return;
            }
            previousGenerated = vietnameseSlug(source.value);
            slug.value = previousGenerated;
        }

        ['input', 'change', 'keyup', 'blur'].forEach(function (eventName) {
            source.addEventListener(eventName, function () {
                updateSlug();
                window.setTimeout(updateSlug, 0);
            });
        });

        if (!slug.value) {
            updateSlug();
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        bindSlug('id_name', 'id_slug');
        bindSlug('id_title', 'id_slug');
    });
})();

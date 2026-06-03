(function () {
    function vietnameseSlug(value) {
        return (value || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/đ/g, 'd')
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

        var previousGenerated = vietnameseSlug(source.value);
        slug.dataset.previousGenerated = previousGenerated;

        source.addEventListener('input', function () {
            var currentGenerated = vietnameseSlug(source.value);
            var previous = slug.dataset.previousGenerated || '';
            var canUpdate = !slug.value || slug.value === previous;

            if (canUpdate) {
                slug.value = currentGenerated;
            }
            slug.dataset.previousGenerated = currentGenerated;
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        bindSlug('id_name', 'id_slug');
        bindSlug('id_title', 'id_slug');
    });
})();

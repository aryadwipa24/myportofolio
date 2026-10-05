let roleConfig = {};
let searchDebounceTimer;
const SEARCH_DEBOUNCE_DELAY = 300;

function initManageRole(config) {
    roleConfig = config;
    setupSearchListeners();
    setupFormSubmitListener();
    fetchRoles();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function fetchRoles() {
    const nonEditorInput = document.getElementById('search-non-editor-input');
    const editorInput = document.getElementById('search-editor-input');

    const nonEditorQuery = nonEditorInput ? nonEditorInput.value.trim() : '';
    const editorQuery = editorInput ? editorInput.value.trim() : '';

    const params = new URLSearchParams({
        'search-non-editor': nonEditorQuery,
        'search-editor': editorQuery
    });

    try {
        const response = await fetch(`${roleConfig.getJsonUrl}?${params.toString()}`, {
            headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) throw new Error('Gagal mengambil data role.');

        const data = await response.json();
        renderUserLists(data.non_editors, data.editors, nonEditorQuery, editorQuery);
    } catch (error) {
        console.error('Error fetching roles:', error);
    }
}

function renderUserLists(nonEditors, editors, nonEditorQuery, editorQuery) {
    const nonEditorContainer = document.getElementById('non-editor-list');
    const editorContainer = document.getElementById('editor-list');

    if (nonEditors.length === 0) {
        nonEditorContainer.innerHTML = `<p class="checkbox-item__label">${nonEditorQuery ? 'Tidak ada user dengan username tersebut.' : 'Tidak ada user biasa.'}</p>`;
    } else {
        nonEditorContainer.innerHTML = nonEditors.map(user => `
            <div class="checkbox-item">
                <input type="checkbox" name="add_editor" id="add-user-${user.id}" value="${user.id}" class="checkbox-item__input">
                <label for="add-user-${user.id}" class="checkbox-item__label">${user.username}</label>
            </div>
        `).join('');
    }

    if (editors.length === 0) {
        editorContainer.innerHTML = `<p class="checkbox-item__label">${editorQuery ? 'Tidak ada user dengan username tersebut.' : 'Tidak ada user editor.'}</p>`;
    } else {
        editorContainer.innerHTML = editors.map(user => `
            <div class="checkbox-item">
                <input type="checkbox" name="remove_editor" id="remove-user-${user.id}" value="${user.id}" class="checkbox-item__input">
                <label for="remove-user-${user.id}" class="checkbox-item__label">${user.username}</label>
            </div>
        `).join('');
    }
}

function setupSearchListeners() {
    const inputs = [
        document.getElementById('search-non-editor-input'),
        document.getElementById('search-editor-input')
    ];

    inputs.forEach(input => {
        if (!input) return;
        
        input.addEventListener('input', function() {
            clearTimeout(searchDebounceTimer);
            searchDebounceTimer = setTimeout(fetchRoles, SEARCH_DEBOUNCE_DELAY);
        });

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                clearTimeout(searchDebounceTimer);
                fetchRoles();
            }
        });
    });
}

function setupFormSubmitListener() {
    const form = document.getElementById('role-form');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) submitBtn.disabled = true;

        try {
            const formData = new FormData(form);
            const response = await fetch(roleConfig.saveRoleUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') || roleConfig.csrfToken
                },
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                if (typeof showToast === 'function') {
                    showToast('Berhasil', 'Role user berhasil diperbarui!', 'success');
                }

                fetchRoles();
            } else {
                if (typeof showToast === 'function') {
                    showToast('Gagal', 'Gagal memperbarui role user.', 'error');
                }
            }
        } catch (error) {
            console.error('Error saving roles:', error);
            if (typeof showToast === 'function') {
                showToast('Gagal', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
            }
        } finally {
            if (submitBtn) submitBtn.disabled = false;
        }
    });
}
document.addEventListener('DOMContentLoaded', function() {
    const transactionTable = document.getElementById('transactionTable');
    
    if (transactionTable) {
        transactionTable.addEventListener('click', function(e) {
            if (e.target.tagName === 'A' && e.target.textContent === 'View Details') {
                e.preventDefault();
                const url = e.target.getAttribute('href');
                fetch(url)
                    .then(response => response.text())
                    .then(html => {
                        const main = document.querySelector('main');
                        main.innerHTML = html;
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    }
});

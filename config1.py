require_once 'vendor/autoload.php';

use League\OAuth2\Client\Provider\Auth0;
use League\OAuth2\Client\Provider\Exception\IdentityProviderException;

$provider = new Auth0([
    'clientId' => 'your_client_id',
    'clientSecret' => 'your_client_secret',
    'redirectUri' => 'http://your-app.com/callback',
    'audience' => 'https://your-authorization-server',
]);

if (!isset($_GET['code'])) {
    // Jika tidak ada kode akses, arahkan pengguna untuk otentikasi
    $authUrl = $provider->getAuthorizationUrl();
    $_SESSION['oauth2state'] = $provider->getState();
    header('Location: ' . $authUrl);
    exit;
} elseif (empty($_GET['state']) || ($_GET['state'] !== $_SESSION['oauth2state'])) {
    // Verifikasi keadaan untuk mencegah serangan CSRF
    unset($_SESSION['oauth2state']);
    exit('Invalid state');
} else {
    // Dapatkan token akses setelah pengguna berhasil otentikasi
    try {
        $token = $provider->getAccessToken('authorization_code', [
            'code' => $_GET['code']
        ]);

        // Gunakan token akses untuk mengambil informasi pengguna
        $user = $provider->getResourceOwner($token);
        print_r($user->toArray());
    } catch (IdentityProviderException $e) {
        exit('Gagal: ' . $e->getMessage());
    }
}

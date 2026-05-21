package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.MutableLiveData;

import com.storepilot.auth.CryptoUtil;
import com.storepilot.core.AppDatabase;
import com.storepilot.core.SessionManager;
import com.storepilot.db.entities.User;
import com.storepilot.repositories.UserRepository;

public class AuthViewModel extends AndroidViewModel {

    private final UserRepository userRepository;
    public final MutableLiveData<String> loginError = new MutableLiveData<>();
    public final MutableLiveData<Boolean> loginSuccess = new MutableLiveData<>();
    public final MutableLiveData<Boolean> setupComplete = new MutableLiveData<>();
    public final MutableLiveData<Boolean> needsSetup = new MutableLiveData<>();

    public AuthViewModel(@NonNull Application application) {
        super(application);
        userRepository = new UserRepository(application);
    }

    public void checkNeedsSetup() {
        AppDatabase.dbExecutor.execute(() -> {
            int ownerCount = userRepository.getOwnerCount();
            needsSetup.postValue(ownerCount == 0);
        });
    }

    public void login(String usernameOrEmail, String password) {
        AppDatabase.dbExecutor.execute(() -> {
            // Try username first, then email (supports both login methods)
            User user = userRepository.findByUsername(usernameOrEmail);
            if (user == null) {
                user = userRepository.findByEmail(usernameOrEmail);
            }
            if (user == null) {
                loginError.postValue("Invalid username or password");
                return;
            }
            if (!CryptoUtil.verifyPassword(password, user.getSalt(), user.getPasswordHash())) {
                loginError.postValue("Invalid username or password");
                return;
            }
            // Save the logged-in user in session
            SessionManager.getInstance().setLoggedInUser(user);
            loginSuccess.postValue(true);
        });
    }

    public void setupOwner(String username, String password, boolean demoMode) {
        AppDatabase.dbExecutor.execute(() -> {
            String salt = CryptoUtil.generateSalt();
            String hash = CryptoUtil.hashPassword(password, salt);
            User owner = new User(username, hash, salt, "OWNER", System.currentTimeMillis());
            userRepository.insert(owner);
            if (demoMode) {
                AppDatabase.getInstance(getApplication()).seedDemoData();
            }
            setupComplete.postValue(true);
        });
    }
}

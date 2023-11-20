/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React, {useEffect} from 'react';
import {VLCPlayer} from 'react-native-vlc-media-player';
// import Orientation from 'react-native-orientation';
// import {Node} from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  useColorScheme,
  Button,
  View,
  Alert,
} from 'react-native';

import {
  Header,
  LearnMoreLinks,
  Colors,
  DebugInstructions,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';
// import {Notifications} from 'react-native-notifications';
// import {getMessaging, getToken} from '@firebase/messaging';
import messaging from '@react-native-firebase/messaging';
import Orientation from 'react-native-orientation';
// import firebase from '@react-native-firebase/app';
import {DarkTheme, NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';

const token = messaging().getToken();
token.then(data => {
  console.log('FCM Token: ' + data);
});

messaging().onTokenRefresh(newToken => {
  console.log('FCM Token Refreshed:', newToken);
});

messaging().setBackgroundMessageHandler(async remoteMessage => {
    // Send a notification alert
  await Alert.alert('SmartHomeSecurity', 'Unknown person detected!');
});

const App1 = ({navigation}) => {
  Orientation.lockToPortrait();
  return (
    <View style={styles.homepage}>
      {/* <View style={{marginRight: 10}}>
        <Button title="Add New Face" />
      </View> */}
      <View>
        <Button
          title="View Camera"
          onPress={() => {
            navigation.navigate('camerafeed');
          }}
        />
      </View>
    </View>
  );
};

const Stack = createNativeStackNavigator();

const App = () => {
  return (
    <NavigationContainer theme={DarkTheme}>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={App1} />
        <Stack.Screen name="camerafeed" component={Homescreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const Homescreen = () => {
  // const credentials = {
  //   clientId:
  //     '638558946991-33vrrklk0mjrhddtmc20jkkpr91da9me.apps.googleusercontent.com',
  //   appId: '1:638558946991:android:a6995640e8363b53c6f65a',
  //   apiKey: 'BDHJ2jZUX_Zfj7imvD8z9pDzzeM0JfAaF_ImfBC9bq6ruELmSYIP3qxY',
  //   databaseURL: '',
  //   storageBucket: 'smarthomesecurity-3e445.appspot.com',
  //   messagingSenderId: '638558946991 ',
  //   projectId: 'smarthomesecurity-3e445',
  // };
  // const config = {
  //   name: 'frontend',
  // };
  useEffect(() => {
    // firebase.initializeApp();
    // const orientation = Orientation.getInitialOrientation();
    // Orientation.lockToLandscape();
    const unsubscribe = messaging().onMessage(async remoteMessage => {
      await Alert.alert('Unknown person detected!');
    });

    return unsubscribe;
  });
  Orientation.lockToLandscape();
  return (
    <View style={styles.container}>
      <StatusBar hidden={true} />
      {/* <Text>Hi mutton</Text> */}
      <VLCPlayer
        style={styles.video}
        // videoAspectRatio="16:9"
        autoplay={true}
        autoAspectRatio={true}
        isLive={true}
        // onProgress={() => {
        //   console.log('onProgress');
        // }}
        autoReloadLive={true}
        // Orientation={}
        source={{
          initType: 2,
          hwDecoderEnabled: 1,
          hwDecoderForced: 1,
          uri: 'rtsp://192.168.1.58:8080/h264.sdp',
          initOptions: [
            // '--no-audio',
            '--rtsp-tcp',
            '--network-caching=150',
            // '--live-caching=150',
            '--rtsp-caching=150',
            '--no-stats',
            '--tcp-caching=150',
            '--realrtsp-caching=150',
          ],
        }}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.Black,
    alignItems: 'center',
    justifyContent: 'center',
  },
  homepage: {
    flex: 1,
    flexDirection: 'row',
    // backgroundColor: Colors.Black,
    rowGap: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: 600,
  },
  sectionDescription: {
    marginTop: 8,
    fontSize: 18,
    fontWeight: 400,
  },
  highlight: {
    fontWeight: 700,
  },
  video: {
    // flex: 1,
    // overflow: 'visible',
    width: '100%',
    height: '100%',
  },
});

export default App;

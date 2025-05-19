// generated from rosidl_generator_cpp/resource/rosidl_generator_cpp__visibility_control.hpp.in
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SVRS__MSG__ROSIDL_GENERATOR_CPP__VISIBILITY_CONTROL_HPP_
#define CUSTOM_MSG_SVRS__MSG__ROSIDL_GENERATOR_CPP__VISIBILITY_CONTROL_HPP_

#ifdef __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define ROSIDL_GENERATOR_CPP_EXPORT_custom_msg_svrs __attribute__ ((dllexport))
    #define ROSIDL_GENERATOR_CPP_IMPORT_custom_msg_svrs __attribute__ ((dllimport))
  #else
    #define ROSIDL_GENERATOR_CPP_EXPORT_custom_msg_svrs __declspec(dllexport)
    #define ROSIDL_GENERATOR_CPP_IMPORT_custom_msg_svrs __declspec(dllimport)
  #endif
  #ifdef ROSIDL_GENERATOR_CPP_BUILDING_DLL_custom_msg_svrs
    #define ROSIDL_GENERATOR_CPP_PUBLIC_custom_msg_svrs ROSIDL_GENERATOR_CPP_EXPORT_custom_msg_svrs
  #else
    #define ROSIDL_GENERATOR_CPP_PUBLIC_custom_msg_svrs ROSIDL_GENERATOR_CPP_IMPORT_custom_msg_svrs
  #endif
#else
  #define ROSIDL_GENERATOR_CPP_EXPORT_custom_msg_svrs __attribute__ ((visibility("default")))
  #define ROSIDL_GENERATOR_CPP_IMPORT_custom_msg_svrs
  #if __GNUC__ >= 4
    #define ROSIDL_GENERATOR_CPP_PUBLIC_custom_msg_svrs __attribute__ ((visibility("default")))
  #else
    #define ROSIDL_GENERATOR_CPP_PUBLIC_custom_msg_svrs
  #endif
#endif

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSG_SVRS__MSG__ROSIDL_GENERATOR_CPP__VISIBILITY_CONTROL_HPP_

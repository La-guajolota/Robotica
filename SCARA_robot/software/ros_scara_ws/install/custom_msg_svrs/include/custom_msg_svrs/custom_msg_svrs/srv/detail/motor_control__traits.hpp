// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msg_svrs:srv/MotorControl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_msg_svrs/srv/motor_control.hpp"


#ifndef CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__TRAITS_HPP_
#define CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_msg_svrs/srv/detail/motor_control__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_msg_svrs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MotorControl_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: data_uint8
  {
    out << "data_uint8: ";
    rosidl_generator_traits::value_to_yaml(msg.data_uint8, out);
    out << ", ";
  }

  // member: data_bool
  {
    out << "data_bool: ";
    rosidl_generator_traits::value_to_yaml(msg.data_bool, out);
    out << ", ";
  }

  // member: data_float
  {
    out << "data_float: ";
    rosidl_generator_traits::value_to_yaml(msg.data_float, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotorControl_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: data_uint8
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "data_uint8: ";
    rosidl_generator_traits::value_to_yaml(msg.data_uint8, out);
    out << "\n";
  }

  // member: data_bool
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "data_bool: ";
    rosidl_generator_traits::value_to_yaml(msg.data_bool, out);
    out << "\n";
  }

  // member: data_float
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "data_float: ";
    rosidl_generator_traits::value_to_yaml(msg.data_float, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotorControl_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_msg_svrs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msg_svrs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msg_svrs::srv::MotorControl_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msg_svrs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msg_svrs::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_msg_svrs::srv::MotorControl_Request & msg)
{
  return custom_msg_svrs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msg_svrs::srv::MotorControl_Request>()
{
  return "custom_msg_svrs::srv::MotorControl_Request";
}

template<>
inline const char * name<custom_msg_svrs::srv::MotorControl_Request>()
{
  return "custom_msg_svrs/srv/MotorControl_Request";
}

template<>
struct has_fixed_size<custom_msg_svrs::srv::MotorControl_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<custom_msg_svrs::srv::MotorControl_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<custom_msg_svrs::srv::MotorControl_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace custom_msg_svrs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MotorControl_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: response_message
  {
    out << "response_message: ";
    rosidl_generator_traits::value_to_yaml(msg.response_message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotorControl_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: response_message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "response_message: ";
    rosidl_generator_traits::value_to_yaml(msg.response_message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotorControl_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_msg_svrs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msg_svrs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msg_svrs::srv::MotorControl_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msg_svrs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msg_svrs::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_msg_svrs::srv::MotorControl_Response & msg)
{
  return custom_msg_svrs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msg_svrs::srv::MotorControl_Response>()
{
  return "custom_msg_svrs::srv::MotorControl_Response";
}

template<>
inline const char * name<custom_msg_svrs::srv::MotorControl_Response>()
{
  return "custom_msg_svrs/srv/MotorControl_Response";
}

template<>
struct has_fixed_size<custom_msg_svrs::srv::MotorControl_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msg_svrs::srv::MotorControl_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_msg_svrs::srv::MotorControl_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace custom_msg_svrs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MotorControl_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotorControl_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotorControl_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_msg_svrs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msg_svrs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msg_svrs::srv::MotorControl_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msg_svrs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msg_svrs::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_msg_svrs::srv::MotorControl_Event & msg)
{
  return custom_msg_svrs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msg_svrs::srv::MotorControl_Event>()
{
  return "custom_msg_svrs::srv::MotorControl_Event";
}

template<>
inline const char * name<custom_msg_svrs::srv::MotorControl_Event>()
{
  return "custom_msg_svrs/srv/MotorControl_Event";
}

template<>
struct has_fixed_size<custom_msg_svrs::srv::MotorControl_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msg_svrs::srv::MotorControl_Event>
  : std::integral_constant<bool, has_bounded_size<custom_msg_svrs::srv::MotorControl_Request>::value && has_bounded_size<custom_msg_svrs::srv::MotorControl_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<custom_msg_svrs::srv::MotorControl_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_msg_svrs::srv::MotorControl>()
{
  return "custom_msg_svrs::srv::MotorControl";
}

template<>
inline const char * name<custom_msg_svrs::srv::MotorControl>()
{
  return "custom_msg_svrs/srv/MotorControl";
}

template<>
struct has_fixed_size<custom_msg_svrs::srv::MotorControl>
  : std::integral_constant<
    bool,
    has_fixed_size<custom_msg_svrs::srv::MotorControl_Request>::value &&
    has_fixed_size<custom_msg_svrs::srv::MotorControl_Response>::value
  >
{
};

template<>
struct has_bounded_size<custom_msg_svrs::srv::MotorControl>
  : std::integral_constant<
    bool,
    has_bounded_size<custom_msg_svrs::srv::MotorControl_Request>::value &&
    has_bounded_size<custom_msg_svrs::srv::MotorControl_Response>::value
  >
{
};

template<>
struct is_service<custom_msg_svrs::srv::MotorControl>
  : std::true_type
{
};

template<>
struct is_service_request<custom_msg_svrs::srv::MotorControl_Request>
  : std::true_type
{
};

template<>
struct is_service_response<custom_msg_svrs::srv::MotorControl_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__TRAITS_HPP_

// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msg_svrs:srv/MotorControl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_msg_svrs/srv/motor_control.hpp"


#ifndef CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__BUILDER_HPP_
#define CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msg_svrs/srv/detail/motor_control__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msg_svrs
{

namespace srv
{

namespace builder
{

class Init_MotorControl_Request_data_float
{
public:
  explicit Init_MotorControl_Request_data_float(::custom_msg_svrs::srv::MotorControl_Request & msg)
  : msg_(msg)
  {}
  ::custom_msg_svrs::srv::MotorControl_Request data_float(::custom_msg_svrs::srv::MotorControl_Request::_data_float_type arg)
  {
    msg_.data_float = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msg_svrs::srv::MotorControl_Request msg_;
};

class Init_MotorControl_Request_data_bool
{
public:
  explicit Init_MotorControl_Request_data_bool(::custom_msg_svrs::srv::MotorControl_Request & msg)
  : msg_(msg)
  {}
  Init_MotorControl_Request_data_float data_bool(::custom_msg_svrs::srv::MotorControl_Request::_data_bool_type arg)
  {
    msg_.data_bool = std::move(arg);
    return Init_MotorControl_Request_data_float(msg_);
  }

private:
  ::custom_msg_svrs::srv::MotorControl_Request msg_;
};

class Init_MotorControl_Request_data_uint8
{
public:
  Init_MotorControl_Request_data_uint8()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorControl_Request_data_bool data_uint8(::custom_msg_svrs::srv::MotorControl_Request::_data_uint8_type arg)
  {
    msg_.data_uint8 = std::move(arg);
    return Init_MotorControl_Request_data_bool(msg_);
  }

private:
  ::custom_msg_svrs::srv::MotorControl_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msg_svrs::srv::MotorControl_Request>()
{
  return custom_msg_svrs::srv::builder::Init_MotorControl_Request_data_uint8();
}

}  // namespace custom_msg_svrs


namespace custom_msg_svrs
{

namespace srv
{

namespace builder
{

class Init_MotorControl_Response_response_message
{
public:
  Init_MotorControl_Response_response_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msg_svrs::srv::MotorControl_Response response_message(::custom_msg_svrs::srv::MotorControl_Response::_response_message_type arg)
  {
    msg_.response_message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msg_svrs::srv::MotorControl_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msg_svrs::srv::MotorControl_Response>()
{
  return custom_msg_svrs::srv::builder::Init_MotorControl_Response_response_message();
}

}  // namespace custom_msg_svrs


namespace custom_msg_svrs
{

namespace srv
{

namespace builder
{

class Init_MotorControl_Event_response
{
public:
  explicit Init_MotorControl_Event_response(::custom_msg_svrs::srv::MotorControl_Event & msg)
  : msg_(msg)
  {}
  ::custom_msg_svrs::srv::MotorControl_Event response(::custom_msg_svrs::srv::MotorControl_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msg_svrs::srv::MotorControl_Event msg_;
};

class Init_MotorControl_Event_request
{
public:
  explicit Init_MotorControl_Event_request(::custom_msg_svrs::srv::MotorControl_Event & msg)
  : msg_(msg)
  {}
  Init_MotorControl_Event_response request(::custom_msg_svrs::srv::MotorControl_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_MotorControl_Event_response(msg_);
  }

private:
  ::custom_msg_svrs::srv::MotorControl_Event msg_;
};

class Init_MotorControl_Event_info
{
public:
  Init_MotorControl_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorControl_Event_request info(::custom_msg_svrs::srv::MotorControl_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_MotorControl_Event_request(msg_);
  }

private:
  ::custom_msg_svrs::srv::MotorControl_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msg_svrs::srv::MotorControl_Event>()
{
  return custom_msg_svrs::srv::builder::Init_MotorControl_Event_info();
}

}  // namespace custom_msg_svrs

#endif  // CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__BUILDER_HPP_

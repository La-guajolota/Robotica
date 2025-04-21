// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_msg_svrs:srv/MotorControl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_msg_svrs/srv/motor_control.hpp"


#ifndef CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__STRUCT_HPP_
#define CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_msg_svrs__srv__MotorControl_Request __attribute__((deprecated))
#else
# define DEPRECATED__custom_msg_svrs__srv__MotorControl_Request __declspec(deprecated)
#endif

namespace custom_msg_svrs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MotorControl_Request_
{
  using Type = MotorControl_Request_<ContainerAllocator>;

  explicit MotorControl_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data_uint8 = 0;
      this->data_bool = false;
      this->data_float = 0.0f;
    }
  }

  explicit MotorControl_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data_uint8 = 0;
      this->data_bool = false;
      this->data_float = 0.0f;
    }
  }

  // field types and members
  using _data_uint8_type =
    uint8_t;
  _data_uint8_type data_uint8;
  using _data_bool_type =
    bool;
  _data_bool_type data_bool;
  using _data_float_type =
    float;
  _data_float_type data_float;

  // setters for named parameter idiom
  Type & set__data_uint8(
    const uint8_t & _arg)
  {
    this->data_uint8 = _arg;
    return *this;
  }
  Type & set__data_bool(
    const bool & _arg)
  {
    this->data_bool = _arg;
    return *this;
  }
  Type & set__data_float(
    const float & _arg)
  {
    this->data_float = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msg_svrs__srv__MotorControl_Request
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msg_svrs__srv__MotorControl_Request
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorControl_Request_ & other) const
  {
    if (this->data_uint8 != other.data_uint8) {
      return false;
    }
    if (this->data_bool != other.data_bool) {
      return false;
    }
    if (this->data_float != other.data_float) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorControl_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorControl_Request_

// alias to use template instance with default allocator
using MotorControl_Request =
  custom_msg_svrs::srv::MotorControl_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_msg_svrs


#ifndef _WIN32
# define DEPRECATED__custom_msg_svrs__srv__MotorControl_Response __attribute__((deprecated))
#else
# define DEPRECATED__custom_msg_svrs__srv__MotorControl_Response __declspec(deprecated)
#endif

namespace custom_msg_svrs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MotorControl_Response_
{
  using Type = MotorControl_Response_<ContainerAllocator>;

  explicit MotorControl_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->response_message = "";
    }
  }

  explicit MotorControl_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : response_message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->response_message = "";
    }
  }

  // field types and members
  using _response_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _response_message_type response_message;

  // setters for named parameter idiom
  Type & set__response_message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->response_message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msg_svrs__srv__MotorControl_Response
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msg_svrs__srv__MotorControl_Response
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorControl_Response_ & other) const
  {
    if (this->response_message != other.response_message) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorControl_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorControl_Response_

// alias to use template instance with default allocator
using MotorControl_Response =
  custom_msg_svrs::srv::MotorControl_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_msg_svrs


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_msg_svrs__srv__MotorControl_Event __attribute__((deprecated))
#else
# define DEPRECATED__custom_msg_svrs__srv__MotorControl_Event __declspec(deprecated)
#endif

namespace custom_msg_svrs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MotorControl_Event_
{
  using Type = MotorControl_Event_<ContainerAllocator>;

  explicit MotorControl_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit MotorControl_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_msg_svrs::srv::MotorControl_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_msg_svrs::srv::MotorControl_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msg_svrs__srv__MotorControl_Event
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msg_svrs__srv__MotorControl_Event
    std::shared_ptr<custom_msg_svrs::srv::MotorControl_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorControl_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorControl_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorControl_Event_

// alias to use template instance with default allocator
using MotorControl_Event =
  custom_msg_svrs::srv::MotorControl_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_msg_svrs

namespace custom_msg_svrs
{

namespace srv
{

struct MotorControl
{
  using Request = custom_msg_svrs::srv::MotorControl_Request;
  using Response = custom_msg_svrs::srv::MotorControl_Response;
  using Event = custom_msg_svrs::srv::MotorControl_Event;
};

}  // namespace srv

}  // namespace custom_msg_svrs

#endif  // CUSTOM_MSG_SVRS__SRV__DETAIL__MOTOR_CONTROL__STRUCT_HPP_

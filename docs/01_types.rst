types
=====

There a three variations of the signal type used internally, however only the
one called simply `signal` is intended to be directly instanciated from code
consuming the module.

signal
    Used to define a signal. Can be seen as the idendity or type of a signal.
    Implements the descriptor protocol to yield a `boundsignal` when accessed 
    as a class member. Has a method `parameterise` that creates a `psignal`

boundsignal
    Represents a signal in a specific context. This type is what typically is
    used as the key when publishing. Contains a reference to it's context (any 
    object) and it's signal (`signal` or `psignal`). Instances are considered 
    equal if their respective signal and context compare equal.

psignal
    A parameterisation of a `signal`. Contains a reference to a `signal` and a 
    tuple of parameter values. If the signal and the parameters are equal two 
    `psignal` instances are considered equal. If the parameter tuple is empty 
    it also compares equal to the root `signal` type. While `psignal` inherits 
    from `signal` this is solely for code reuse and it does aim to comply with 
    liskov substitution.

::

      +--------+
      | signal |
      +--------+
        |     \ 
  +---------+  |
  | psignal |  |
  +---------+  |
         \     |
          \    |
           \   |
       +-------------+
       | boundsignal |
       +-------------+


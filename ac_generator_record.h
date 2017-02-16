/*
 *  ac_generator.h
 *
 *  This file is part of NEST.
 *
 *  Copyright (C) 2004 The NEST Initiative
 *
 *  NEST is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  NEST is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with NEST.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#ifndef AC_GENERATOR_H
#define AC_GENERATOR_H

// provides AC input current

#include "nest.h"
#include "event.h"
#include "node.h"
#include "connection.h"
#include "stimulating_device.h"
#include "universal_data_logger.h"  // issue #658

/* BeginDocumentation
   Name: ac_generator - provides AC input current
   Description:

   This device produce an ac-current which are sent by a current event.
   The parameters are
   amplitude   double -  Amplitude of sine current in pA
   offset      double -  Constant amplitude offset in pA
   phase       double -  Phase of sine current (0-360 deg)
   frequency   double -  Frequency in Hz
   4) The

   The currents are updated every time step by exact integration schemes from [1]

   References:
   [1] S. Rotter and M. Diesmann, Exact digital simulation of time-
   invariant linear systems with applications to neuronal modeling,
   Biol. Cybern. 81, 381-402 (1999)

   Sends: CurrentEvent

   Author: Johan Hake, Spring 2003

   SeeAlso: Device, StimulatingDevice, dc_generator
*/

namespace nest
{

class Network;

class ac_generator : public Node
{

public:
  ac_generator();
  ac_generator( const ac_generator& );

  bool
  has_proxies() const
  {
    return false;
  }

  port send_test_event( Node&, rport, synindex, bool );

  using Node::handle;                                       // issue #658
  using Node::handles_test_event;                           // issue #658

  void handle( DataLoggingRequest& );                       // issue #658

  port handles_test_event( DataLoggingRequest&, rport );    // issue #658

  void get_status( DictionaryDatum& ) const;
  void set_status( const DictionaryDatum& );

  // method added for issue #658
  //! Allow multimeter to connect to local instances
  bool
  local_receiver() const
  {
    return true;
  }

private:
  void init_state_( const Node& );
  void init_buffers_();
  void calibrate();

  void update( Time const&, const long_t, const long_t );


  // ------------------------------------------------------------

  struct Parameters_
  {
    double_t amp_;     //!< Amplitude of sine-current
    double_t offset_;  //!< Offset of sine-current
    double_t freq_;    //!< Standard frequency in Hz
    double_t phi_deg_; //!< Phase of sine current (0-360 deg)

    Parameters_(); //!< Sets default parameter values
    Parameters_( const Parameters_& );                                        // issue #658
    Parameters_& operator=( const Parameters_& p ); // Copy constructor EN    // issue #658

    void get( DictionaryDatum& ) const; //!< Store current values in dictionary
    void set( const DictionaryDatum& ); //!< Set values from dicitonary
  };

  // ------------------------------------------------------------

  struct State_
  {
    double_t y_0_;
    double_t y_1_;

    double_t inj_;          // issue #658

    State_(); //!< Sets default parameter values

    void get( DictionaryDatum& ) const; //!< Store current values in dictionary
  };

  // ------------------------------------------------------------

  // block added for issue #658
  // These friend declarations must be precisely here.
  friend class RecordablesMap< ac_generator >;
  friend class UniversalDataLogger< ac_generator >;

  // ------------------------------------------------------------

  // block added for issue #658
  /**
   * Buffers of the model.
   */
  struct Buffers_
  {
    Buffers_( ac_generator& );
    Buffers_( const Buffers_&, ac_generator& );
    UniversalDataLogger< ac_generator > logger_;
  };

  // ------------------------------------------------------------

  struct Variables_
  {
    double_t omega_;   //!< Angelfrequency i rad/s
    double_t phi_rad_; //!< Phase of sine current (0-2Pi rad)

    // The exact integration matrix
    double_t A_00_;
    double_t A_01_;
    double_t A_10_;
    double_t A_11_;
  };

  // method added for issue #658
  double_t
  get_inj_() const
  {
    return S_.inj_;
  }

  // ------------------------------------------------------------

  StimulatingDevice< CurrentEvent > device_;
  static RecordablesMap< ac_generator > recordablesMap_;    // issue #658

  Parameters_ P_;
  State_ S_;
  Variables_ V_;
  Buffers_ B_;                                              // issue #658
};

inline port
ac_generator::send_test_event( Node& target, rport receptor_type, synindex syn_id, bool )
{
  device_.enforce_single_syn_type( syn_id );

  CurrentEvent e;
  e.set_sender( *this );

  return target.handles_test_event( e, receptor_type );
}

// method added for issue #658
inline port
ac_generator::handles_test_event( DataLoggingRequest& dlr, rport receptor_type )
{
  if ( receptor_type != 0 )
    throw UnknownReceptorType( receptor_type, get_name() );
  return B_.logger_.connect_logging_device( dlr, recordablesMap_ );
}

inline void
ac_generator::get_status( DictionaryDatum& d ) const
{
  P_.get( d );
  S_.get( d );
  device_.get_status( d );
  ( *d )[ names::recordables ] = recordablesMap_.get_list();    // issue #658
}

inline void
ac_generator::set_status( const DictionaryDatum& d )
{
  Parameters_ ptmp = P_; // temporary copy in case of errors
  ptmp.set( d );         // throws if BadProperty

  // State_ is read-only

  // We now know that ptmp is consistent. We do not write it back
  // to P_ before we are also sure that the properties to be set
  // in the parent class are internally consistent.
  device_.set_status( d );

  // if we get here, temporaries contain consistent set of properties
  P_ = ptmp;
}
}
#endif // AC_GENERATOR_H
